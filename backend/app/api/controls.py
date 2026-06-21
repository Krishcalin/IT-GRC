"""ISO 27001 Controls routes."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models.control import Control
from ..models.control_mapping import ControlMapping
from ..models.user import User
from ..models.activity_log import ActivityLog
from ..schemas.control import (
    ControlCreate, ControlUpdate, ControlRead, ControlMappingCreate, ControlMappingRead,
)
from .deps import get_current_user, require_superuser

router = APIRouter()


@router.get("/", response_model=list[ControlRead])
async def list_controls(
    theme: str | None = None,
    status: str | None = None,
    framework: str | None = None,
    search: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(200, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    q = select(Control)
    if theme:
        q = q.where(Control.theme == theme)
    if status:
        q = q.where(Control.status == status)
    if framework:
        q = q.where(Control.framework == framework)
    if search:
        q = q.where(or_(Control.clause.ilike(f"%{search}%"), Control.title.ilike(f"%{search}%")))
    q = q.order_by(Control.clause).offset(skip).limit(limit)
    rows = (await db.execute(q)).scalars().all()
    return rows


@router.get("/{control_id}", response_model=ControlRead)
async def get_control(control_id: UUID, db: AsyncSession = Depends(get_db)):
    ctrl = (await db.execute(select(Control).where(Control.id == control_id))).scalar_one_or_none()
    if not ctrl:
        raise HTTPException(404, "Control not found")
    return ctrl


@router.get("/{control_id}/mappings", response_model=list[ControlMappingRead])
async def list_control_mappings(control_id: UUID, db: AsyncSession = Depends(get_db)):
    """Cross-framework mappings for a control (both directions)."""
    ctrl = (await db.execute(select(Control).where(Control.id == control_id))).scalar_one_or_none()
    if not ctrl:
        raise HTTPException(404, "Control not found")
    rows = (await db.execute(
        select(ControlMapping).where(
            or_(ControlMapping.source_control_id == control_id, ControlMapping.target_control_id == control_id)
        )
    )).scalars().all()
    out = []
    for m in rows:
        if m.source_control_id == control_id:
            other, direction = m.target_control, "outgoing"
        else:
            other, direction = m.source_control, "incoming"
        out.append({"id": m.id, "relationship_type": m.relationship_type, "note": m.note, "direction": direction, "control": other})
    return out


@router.post("/{control_id}/mappings", response_model=ControlMappingRead, status_code=201)
async def create_control_mapping(
    control_id: UUID,
    body: ControlMappingCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if control_id == body.target_control_id:
        raise HTTPException(422, "A control cannot be mapped to itself")
    src = (await db.execute(select(Control).where(Control.id == control_id))).scalar_one_or_none()
    tgt = (await db.execute(select(Control).where(Control.id == body.target_control_id))).scalar_one_or_none()
    if not src or not tgt:
        raise HTTPException(404, "Control not found")
    existing = (await db.execute(select(ControlMapping).where(
        or_(
            (ControlMapping.source_control_id == control_id) & (ControlMapping.target_control_id == body.target_control_id),
            (ControlMapping.source_control_id == body.target_control_id) & (ControlMapping.target_control_id == control_id),
        )
    ))).scalar_one_or_none()
    if existing:
        raise HTTPException(409, "Mapping already exists")
    m = ControlMapping(source_control_id=control_id, target_control_id=body.target_control_id,
                       relationship_type=body.relationship_type, note=body.note)
    db.add(m)
    await db.flush()
    await db.refresh(m)
    db.add(ActivityLog(user_id=current_user.id, action="MAP", resource_type="control", resource_id=str(control_id)))
    return {"id": m.id, "relationship_type": m.relationship_type, "note": m.note, "direction": "outgoing", "control": tgt}


@router.delete("/{control_id}/mappings/{mapping_id}", status_code=204)
async def delete_control_mapping(
    control_id: UUID,
    mapping_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    m = (await db.execute(select(ControlMapping).where(ControlMapping.id == mapping_id))).scalar_one_or_none()
    if not m or control_id not in (m.source_control_id, m.target_control_id):
        raise HTTPException(404, "Mapping not found")
    db.add(ActivityLog(user_id=current_user.id, action="UNMAP", resource_type="control", resource_id=str(control_id)))
    await db.delete(m)


@router.post("/", response_model=ControlRead, status_code=201)
async def create_control(
    body: ControlCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ctrl = Control(**body.model_dump())
    db.add(ctrl)
    await db.flush()
    await db.refresh(ctrl)
    db.add(ActivityLog(user_id=current_user.id, action="CREATE", resource_type="control", resource_id=str(ctrl.id)))
    return ctrl


@router.put("/{control_id}", response_model=ControlRead)
async def update_control(
    control_id: UUID,
    body: ControlUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ctrl = (await db.execute(select(Control).where(Control.id == control_id))).scalar_one_or_none()
    if not ctrl:
        raise HTTPException(404, "Control not found")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(ctrl, k, v)
    await db.flush()
    await db.refresh(ctrl)
    db.add(ActivityLog(user_id=current_user.id, action="UPDATE", resource_type="control", resource_id=str(ctrl.id)))
    return ctrl


@router.delete("/{control_id}", status_code=204)
async def delete_control(
    control_id: UUID,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_superuser),
):
    ctrl = (await db.execute(select(Control).where(Control.id == control_id))).scalar_one_or_none()
    if not ctrl:
        raise HTTPException(404, "Control not found")
    db.add(ActivityLog(user_id=admin.id, action="DELETE", resource_type="control", resource_id=str(ctrl.id)))
    await db.delete(ctrl)
