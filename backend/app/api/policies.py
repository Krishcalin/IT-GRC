"""Policy management routes."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models.policy import Policy, PolicyAcknowledgment
from ..models.user import User
from ..models.activity_log import ActivityLog
from ..schemas.policy import PolicyCreate, PolicyUpdate, PolicyRead, PolicyAckRead
from .deps import get_current_user

router = APIRouter()


@router.get("/", response_model=list[PolicyRead])
async def list_policies(
    status: str | None = None,
    category: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    q = select(Policy)
    if status:
        q = q.where(Policy.status == status)
    if category:
        q = q.where(Policy.category == category)
    q = q.order_by(Policy.ref_id).offset(skip).limit(limit)
    return (await db.execute(q)).scalars().all()


@router.post("/", response_model=PolicyRead, status_code=201)
async def create_policy(
    body: PolicyCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    count = (await db.execute(select(func.count()).select_from(Policy))).scalar() or 0
    ref_id = f"POL-{count + 1:03d}"
    policy = Policy(**body.model_dump(), ref_id=ref_id)
    db.add(policy)
    await db.flush()
    await db.refresh(policy)
    db.add(ActivityLog(user_id=current_user.id, action="CREATE", resource_type="policy", resource_id=str(policy.id)))
    return policy


@router.get("/{policy_id}", response_model=PolicyRead)
async def get_policy(policy_id: UUID, db: AsyncSession = Depends(get_db)):
    policy = (await db.execute(select(Policy).where(Policy.id == policy_id))).scalar_one_or_none()
    if not policy:
        raise HTTPException(404, "Policy not found")
    return policy


@router.put("/{policy_id}", response_model=PolicyRead)
async def update_policy(
    policy_id: UUID,
    body: PolicyUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    policy = (await db.execute(select(Policy).where(Policy.id == policy_id))).scalar_one_or_none()
    if not policy:
        raise HTTPException(404, "Policy not found")

    data = body.model_dump(exclude_unset=True)
    # If status is being set to Approved, record approval
    if data.get("status") == "Approved" and policy.status != "Approved":
        data["approved_by"] = current_user.id
        data["approved_at"] = datetime.now(timezone.utc)

    for k, v in data.items():
        setattr(policy, k, v)
    await db.flush()
    await db.refresh(policy)
    db.add(ActivityLog(user_id=current_user.id, action="UPDATE", resource_type="policy", resource_id=str(policy.id)))
    return policy


@router.delete("/{policy_id}", status_code=204)
async def delete_policy(
    policy_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    policy = (await db.execute(select(Policy).where(Policy.id == policy_id))).scalar_one_or_none()
    if not policy:
        raise HTTPException(404, "Policy not found")
    db.add(ActivityLog(user_id=current_user.id, action="DELETE", resource_type="policy", resource_id=str(policy.id)))
    await db.delete(policy)


@router.post("/{policy_id}/acknowledge", response_model=PolicyAckRead, status_code=201)
async def acknowledge_policy(
    policy_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    policy = (await db.execute(select(Policy).where(Policy.id == policy_id))).scalar_one_or_none()
    if not policy:
        raise HTTPException(404, "Policy not found")
    existing = (await db.execute(
        select(PolicyAcknowledgment).where(
            PolicyAcknowledgment.policy_id == policy_id,
            PolicyAcknowledgment.user_id == current_user.id,
        )
    )).scalar_one_or_none()
    if existing:
        raise HTTPException(409, "Already acknowledged")
    ack = PolicyAcknowledgment(policy_id=policy_id, user_id=current_user.id)
    db.add(ack)
    await db.flush()
    await db.refresh(ack)
    return ack


@router.get("/{policy_id}/acknowledgments", response_model=list[PolicyAckRead])
async def list_acknowledgments(policy_id: UUID, db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(
        select(PolicyAcknowledgment).where(PolicyAcknowledgment.policy_id == policy_id)
    )).scalars().all()
    return rows
