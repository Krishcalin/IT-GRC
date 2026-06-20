"""Interested parties (Clause 4.2) routes."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models.interested_party import InterestedParty
from ..models.user import User
from ..models.activity_log import ActivityLog
from ..schemas.interested_party import (
    InterestedPartyCreate,
    InterestedPartyUpdate,
    InterestedPartyRead,
)
from .deps import get_current_user

router = APIRouter()


@router.get("/", response_model=list[InterestedPartyRead])
async def list_interested_parties(
    party_type: str | None = None,
    category: str | None = None,
    search: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(200, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    q = select(InterestedParty)
    if party_type:
        q = q.where(InterestedParty.party_type == party_type)
    if category:
        q = q.where(InterestedParty.category == category)
    if search:
        q = q.where(or_(
            InterestedParty.ref_id.ilike(f"%{search}%"),
            InterestedParty.name.ilike(f"%{search}%"),
        ))
    q = q.order_by(InterestedParty.ref_id).offset(skip).limit(limit)
    return (await db.execute(q)).scalars().all()


@router.post("/", response_model=InterestedPartyRead, status_code=201)
async def create_interested_party(
    body: InterestedPartyCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    count = (await db.execute(select(func.count()).select_from(InterestedParty))).scalar() or 0
    ref_id = f"PARTY-{count + 1:03d}"
    party = InterestedParty(**body.model_dump(), ref_id=ref_id)
    db.add(party)
    await db.flush()
    await db.refresh(party)
    db.add(ActivityLog(user_id=current_user.id, action="CREATE", resource_type="interested_party", resource_id=str(party.id)))
    return party


@router.get("/{party_id}", response_model=InterestedPartyRead)
async def get_interested_party(party_id: UUID, db: AsyncSession = Depends(get_db)):
    party = (await db.execute(select(InterestedParty).where(InterestedParty.id == party_id))).scalar_one_or_none()
    if not party:
        raise HTTPException(404, "Interested party not found")
    return party


@router.put("/{party_id}", response_model=InterestedPartyRead)
async def update_interested_party(
    party_id: UUID,
    body: InterestedPartyUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    party = (await db.execute(select(InterestedParty).where(InterestedParty.id == party_id))).scalar_one_or_none()
    if not party:
        raise HTTPException(404, "Interested party not found")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(party, k, v)
    await db.flush()
    await db.refresh(party)
    db.add(ActivityLog(user_id=current_user.id, action="UPDATE", resource_type="interested_party", resource_id=str(party.id)))
    return party


@router.delete("/{party_id}", status_code=204)
async def delete_interested_party(
    party_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    party = (await db.execute(select(InterestedParty).where(InterestedParty.id == party_id))).scalar_one_or_none()
    if not party:
        raise HTTPException(404, "Interested party not found")
    db.add(ActivityLog(user_id=current_user.id, action="DELETE", resource_type="interested_party", resource_id=str(party.id)))
    await db.delete(party)
