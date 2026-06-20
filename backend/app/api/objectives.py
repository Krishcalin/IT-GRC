"""Information security objectives (Clause 6.2) routes."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models.objective import Objective
from ..models.user import User
from ..models.activity_log import ActivityLog
from ..schemas.objective import ObjectiveCreate, ObjectiveUpdate, ObjectiveRead
from .deps import get_current_user

router = APIRouter()


@router.get("/", response_model=list[ObjectiveRead])
async def list_objectives(
    status: str | None = None,
    search: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(200, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    q = select(Objective)
    if status:
        q = q.where(Objective.status == status)
    if search:
        q = q.where(or_(Objective.ref_id.ilike(f"%{search}%"), Objective.title.ilike(f"%{search}%")))
    q = q.order_by(Objective.ref_id).offset(skip).limit(limit)
    return (await db.execute(q)).scalars().all()


@router.post("/", response_model=ObjectiveRead, status_code=201)
async def create_objective(
    body: ObjectiveCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    count = (await db.execute(select(func.count()).select_from(Objective))).scalar() or 0
    ref_id = f"OBJ-{count + 1:03d}"
    obj = Objective(**body.model_dump(), ref_id=ref_id)
    db.add(obj)
    await db.flush()
    await db.refresh(obj)
    db.add(ActivityLog(user_id=current_user.id, action="CREATE", resource_type="objective", resource_id=str(obj.id)))
    return obj


@router.get("/{objective_id}", response_model=ObjectiveRead)
async def get_objective(objective_id: UUID, db: AsyncSession = Depends(get_db)):
    obj = (await db.execute(select(Objective).where(Objective.id == objective_id))).scalar_one_or_none()
    if not obj:
        raise HTTPException(404, "Objective not found")
    return obj


@router.put("/{objective_id}", response_model=ObjectiveRead)
async def update_objective(
    objective_id: UUID,
    body: ObjectiveUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = (await db.execute(select(Objective).where(Objective.id == objective_id))).scalar_one_or_none()
    if not obj:
        raise HTTPException(404, "Objective not found")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    await db.flush()
    await db.refresh(obj)
    db.add(ActivityLog(user_id=current_user.id, action="UPDATE", resource_type="objective", resource_id=str(obj.id)))
    return obj


@router.delete("/{objective_id}", status_code=204)
async def delete_objective(
    objective_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = (await db.execute(select(Objective).where(Objective.id == objective_id))).scalar_one_or_none()
    if not obj:
        raise HTTPException(404, "Objective not found")
    db.add(ActivityLog(user_id=current_user.id, action="DELETE", resource_type="objective", resource_id=str(obj.id)))
    await db.delete(obj)
