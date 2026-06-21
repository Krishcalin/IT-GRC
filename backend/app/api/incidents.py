"""Information security incident (Clauses 5.24–5.28) routes."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models.incident import Incident
from ..models.user import User
from ..models.activity_log import ActivityLog
from ..schemas.incident import IncidentCreate, IncidentUpdate, IncidentRead
from .deps import get_current_user

router = APIRouter()


@router.get("/", response_model=list[IncidentRead])
async def list_incidents(
    category: str | None = None,
    severity: str | None = None,
    status: str | None = None,
    risk_id: UUID | None = None,
    search: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(200, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    q = select(Incident)
    if category:
        q = q.where(Incident.category == category)
    if severity:
        q = q.where(Incident.severity == severity)
    if status:
        q = q.where(Incident.status == status)
    if risk_id:
        q = q.where(Incident.risk_id == risk_id)
    if search:
        q = q.where(or_(Incident.ref_id.ilike(f"%{search}%"), Incident.title.ilike(f"%{search}%")))
    q = q.order_by(Incident.ref_id.desc()).offset(skip).limit(limit)
    return (await db.execute(q)).scalars().all()


@router.post("/", response_model=IncidentRead, status_code=201)
async def create_incident(
    body: IncidentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    count = (await db.execute(select(func.count()).select_from(Incident))).scalar() or 0
    ref_id = f"INC-{count + 1:03d}"
    incident = Incident(**body.model_dump(), ref_id=ref_id)
    db.add(incident)
    await db.flush()
    await db.refresh(incident)
    db.add(ActivityLog(user_id=current_user.id, action="CREATE", resource_type="incident", resource_id=str(incident.id)))
    return incident


@router.get("/{incident_id}", response_model=IncidentRead)
async def get_incident(incident_id: UUID, db: AsyncSession = Depends(get_db)):
    incident = (await db.execute(select(Incident).where(Incident.id == incident_id))).scalar_one_or_none()
    if not incident:
        raise HTTPException(404, "Incident not found")
    return incident


@router.put("/{incident_id}", response_model=IncidentRead)
async def update_incident(
    incident_id: UUID,
    body: IncidentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    incident = (await db.execute(select(Incident).where(Incident.id == incident_id))).scalar_one_or_none()
    if not incident:
        raise HTTPException(404, "Incident not found")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(incident, k, v)
    await db.flush()
    await db.refresh(incident)
    db.add(ActivityLog(user_id=current_user.id, action="UPDATE", resource_type="incident", resource_id=str(incident.id)))
    return incident


@router.delete("/{incident_id}", status_code=204)
async def delete_incident(
    incident_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    incident = (await db.execute(select(Incident).where(Incident.id == incident_id))).scalar_one_or_none()
    if not incident:
        raise HTTPException(404, "Incident not found")
    db.add(ActivityLog(user_id=current_user.id, action="DELETE", resource_type="incident", resource_id=str(incident.id)))
    await db.delete(incident)
