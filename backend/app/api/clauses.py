"""ISO 27001:2022 management-system clause (Clauses 4–10) routes."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models.clause_requirement import ClauseRequirement
from ..models.user import User
from ..models.activity_log import ActivityLog
from ..schemas.clause_requirement import (
    ClauseRequirementCreate,
    ClauseRequirementUpdate,
    ClauseRequirementRead,
)
from .deps import get_current_user, require_superuser

router = APIRouter()


@router.get("/", response_model=list[ClauseRequirementRead])
async def list_clauses(
    section: str | None = None,
    clause_number: int | None = None,
    status: str | None = None,
    search: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    q = select(ClauseRequirement)
    if section:
        q = q.where(ClauseRequirement.section == section)
    if clause_number:
        q = q.where(ClauseRequirement.clause_number == clause_number)
    if status:
        q = q.where(ClauseRequirement.conformity_status == status)
    if search:
        q = q.where(or_(
            ClauseRequirement.clause.ilike(f"%{search}%"),
            ClauseRequirement.title.ilike(f"%{search}%"),
        ))
    q = q.order_by(ClauseRequirement.clause_number, ClauseRequirement.clause).offset(skip).limit(limit)
    rows = (await db.execute(q)).scalars().all()
    return rows


@router.get("/{clause_id}", response_model=ClauseRequirementRead)
async def get_clause(clause_id: UUID, db: AsyncSession = Depends(get_db)):
    row = (await db.execute(
        select(ClauseRequirement).where(ClauseRequirement.id == clause_id)
    )).scalar_one_or_none()
    if not row:
        raise HTTPException(404, "Clause requirement not found")
    return row


@router.post("/", response_model=ClauseRequirementRead, status_code=201)
async def create_clause(
    body: ClauseRequirementCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    row = ClauseRequirement(**body.model_dump())
    db.add(row)
    await db.flush()
    await db.refresh(row)
    db.add(ActivityLog(user_id=current_user.id, action="CREATE", resource_type="clause", resource_id=str(row.id)))
    return row


@router.put("/{clause_id}", response_model=ClauseRequirementRead)
async def update_clause(
    clause_id: UUID,
    body: ClauseRequirementUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    row = (await db.execute(
        select(ClauseRequirement).where(ClauseRequirement.id == clause_id)
    )).scalar_one_or_none()
    if not row:
        raise HTTPException(404, "Clause requirement not found")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(row, k, v)
    await db.flush()
    await db.refresh(row)
    db.add(ActivityLog(user_id=current_user.id, action="UPDATE", resource_type="clause", resource_id=str(row.id)))
    return row


@router.delete("/{clause_id}", status_code=204)
async def delete_clause(
    clause_id: UUID,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_superuser),
):
    row = (await db.execute(
        select(ClauseRequirement).where(ClauseRequirement.id == clause_id)
    )).scalar_one_or_none()
    if not row:
        raise HTTPException(404, "Clause requirement not found")
    db.add(ActivityLog(user_id=admin.id, action="DELETE", resource_type="clause", resource_id=str(row.id)))
    await db.delete(row)
