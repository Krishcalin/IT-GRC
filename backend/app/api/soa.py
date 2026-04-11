"""Statement of Applicability routes."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models.soa import SoAEntry
from ..models.user import User
from ..models.activity_log import ActivityLog
from ..schemas.soa import SoACreate, SoAUpdate, SoARead
from .deps import get_current_user

router = APIRouter()


@router.get("/", response_model=list[SoARead])
async def list_soa(
    applicable: bool | None = None,
    implementation_status: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(200, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    q = select(SoAEntry)
    if applicable is not None:
        q = q.where(SoAEntry.applicable == applicable)
    if implementation_status:
        q = q.where(SoAEntry.implementation_status == implementation_status)
    q = q.offset(skip).limit(limit)
    return (await db.execute(q)).scalars().all()


@router.post("/", response_model=SoARead, status_code=201)
async def create_soa(
    body: SoACreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = (await db.execute(select(SoAEntry).where(SoAEntry.control_id == body.control_id))).scalar_one_or_none()
    if existing:
        raise HTTPException(409, "SoA entry already exists for this control")
    entry = SoAEntry(**body.model_dump())
    db.add(entry)
    await db.flush()
    await db.refresh(entry)
    db.add(ActivityLog(user_id=current_user.id, action="CREATE", resource_type="soa", resource_id=str(entry.id)))
    return entry


@router.put("/{soa_id}", response_model=SoARead)
async def update_soa(
    soa_id: UUID,
    body: SoAUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    entry = (await db.execute(select(SoAEntry).where(SoAEntry.id == soa_id))).scalar_one_or_none()
    if not entry:
        raise HTTPException(404, "SoA entry not found")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(entry, k, v)
    await db.flush()
    await db.refresh(entry)
    db.add(ActivityLog(user_id=current_user.id, action="UPDATE", resource_type="soa", resource_id=str(entry.id)))
    return entry


@router.get("/export", response_model=list[SoARead])
async def export_soa(db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(SoAEntry))).scalars().all()
    return rows
