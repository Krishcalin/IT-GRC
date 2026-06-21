"""Awareness & training (Clauses 7.2 / 7.3) routes — campaigns + participation records."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models.training import TrainingCampaign, TrainingRecord
from ..models.user import User
from ..models.activity_log import ActivityLog
from ..schemas.training import (
    TrainingCampaignCreate, TrainingCampaignUpdate, TrainingCampaignRead,
    TrainingRecordCreate, TrainingRecordUpdate, TrainingRecordRead,
)
from .deps import get_current_user

router = APIRouter()


# ── Campaigns ─────────────────────────────────────────────
@router.get("/", response_model=list[TrainingCampaignRead])
async def list_campaigns(
    training_type: str | None = None,
    status: str | None = None,
    search: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(200, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    q = select(TrainingCampaign)
    if training_type:
        q = q.where(TrainingCampaign.training_type == training_type)
    if status:
        q = q.where(TrainingCampaign.status == status)
    if search:
        q = q.where(or_(TrainingCampaign.ref_id.ilike(f"%{search}%"), TrainingCampaign.title.ilike(f"%{search}%")))
    q = q.order_by(TrainingCampaign.ref_id).offset(skip).limit(limit)
    return (await db.execute(q)).scalars().all()


@router.post("/", response_model=TrainingCampaignRead, status_code=201)
async def create_campaign(
    body: TrainingCampaignCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    count = (await db.execute(select(func.count()).select_from(TrainingCampaign))).scalar() or 0
    ref_id = f"TRN-{count + 1:03d}"
    campaign = TrainingCampaign(**body.model_dump(), ref_id=ref_id)
    db.add(campaign)
    await db.flush()
    await db.refresh(campaign)
    db.add(ActivityLog(user_id=current_user.id, action="CREATE", resource_type="training_campaign", resource_id=str(campaign.id)))
    return campaign


@router.get("/{campaign_id}", response_model=TrainingCampaignRead)
async def get_campaign(campaign_id: UUID, db: AsyncSession = Depends(get_db)):
    campaign = (await db.execute(select(TrainingCampaign).where(TrainingCampaign.id == campaign_id))).scalar_one_or_none()
    if not campaign:
        raise HTTPException(404, "Training campaign not found")
    return campaign


@router.put("/{campaign_id}", response_model=TrainingCampaignRead)
async def update_campaign(
    campaign_id: UUID,
    body: TrainingCampaignUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    campaign = (await db.execute(select(TrainingCampaign).where(TrainingCampaign.id == campaign_id))).scalar_one_or_none()
    if not campaign:
        raise HTTPException(404, "Training campaign not found")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(campaign, k, v)
    await db.flush()
    await db.refresh(campaign)
    db.add(ActivityLog(user_id=current_user.id, action="UPDATE", resource_type="training_campaign", resource_id=str(campaign.id)))
    return campaign


@router.delete("/{campaign_id}", status_code=204)
async def delete_campaign(
    campaign_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    campaign = (await db.execute(select(TrainingCampaign).where(TrainingCampaign.id == campaign_id))).scalar_one_or_none()
    if not campaign:
        raise HTTPException(404, "Training campaign not found")
    db.add(ActivityLog(user_id=current_user.id, action="DELETE", resource_type="training_campaign", resource_id=str(campaign.id)))
    await db.delete(campaign)


# ── Participation records ─────────────────────────────────
@router.post("/{campaign_id}/records", response_model=TrainingRecordRead, status_code=201)
async def add_record(
    campaign_id: UUID,
    body: TrainingRecordCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    campaign = (await db.execute(select(TrainingCampaign).where(TrainingCampaign.id == campaign_id))).scalar_one_or_none()
    if not campaign:
        raise HTTPException(404, "Training campaign not found")
    count = (await db.execute(select(func.count()).select_from(TrainingRecord))).scalar() or 0
    ref_id = f"TRR-{count + 1:03d}"
    record = TrainingRecord(**body.model_dump(), campaign_id=campaign_id, ref_id=ref_id)
    db.add(record)
    await db.flush()
    await db.refresh(record)
    db.add(ActivityLog(user_id=current_user.id, action="CREATE", resource_type="training_record", resource_id=str(record.id)))
    return record


@router.put("/records/{record_id}", response_model=TrainingRecordRead)
async def update_record(
    record_id: UUID,
    body: TrainingRecordUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = (await db.execute(select(TrainingRecord).where(TrainingRecord.id == record_id))).scalar_one_or_none()
    if not record:
        raise HTTPException(404, "Training record not found")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(record, k, v)
    await db.flush()
    await db.refresh(record)
    db.add(ActivityLog(user_id=current_user.id, action="UPDATE", resource_type="training_record", resource_id=str(record.id)))
    return record


@router.delete("/records/{record_id}", status_code=204)
async def delete_record(
    record_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = (await db.execute(select(TrainingRecord).where(TrainingRecord.id == record_id))).scalar_one_or_none()
    if not record:
        raise HTTPException(404, "Training record not found")
    db.add(ActivityLog(user_id=current_user.id, action="DELETE", resource_type="training_record", resource_id=str(record.id)))
    await db.delete(record)
