"""Asset inventory routes."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models.asset import Asset, AssetRisk
from ..models.risk import Risk
from ..models.user import User
from ..models.activity_log import ActivityLog
from ..schemas.asset import AssetCreate, AssetUpdate, AssetRead
from .deps import get_current_user

router = APIRouter()


@router.get("/", response_model=list[AssetRead])
async def list_assets(
    asset_type: str | None = None,
    classification: str | None = None,
    status: str | None = None,
    criticality: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    q = select(Asset)
    if asset_type:
        q = q.where(Asset.asset_type == asset_type)
    if classification:
        q = q.where(Asset.classification == classification)
    if status:
        q = q.where(Asset.status == status)
    if criticality:
        q = q.where(Asset.criticality == criticality)
    q = q.order_by(Asset.ref_id).offset(skip).limit(limit)
    return (await db.execute(q)).scalars().all()


@router.post("/", response_model=AssetRead, status_code=201)
async def create_asset(
    body: AssetCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    count = (await db.execute(select(func.count()).select_from(Asset))).scalar() or 0
    ref_id = f"ASSET-{count + 1:03d}"
    asset = Asset(**body.model_dump(), ref_id=ref_id)
    db.add(asset)
    await db.flush()
    await db.refresh(asset)
    db.add(ActivityLog(user_id=current_user.id, action="CREATE", resource_type="asset", resource_id=str(asset.id)))
    return asset


@router.get("/{asset_id}", response_model=AssetRead)
async def get_asset(asset_id: UUID, db: AsyncSession = Depends(get_db)):
    asset = (await db.execute(select(Asset).where(Asset.id == asset_id))).scalar_one_or_none()
    if not asset:
        raise HTTPException(404, "Asset not found")
    return asset


@router.put("/{asset_id}", response_model=AssetRead)
async def update_asset(
    asset_id: UUID,
    body: AssetUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    asset = (await db.execute(select(Asset).where(Asset.id == asset_id))).scalar_one_or_none()
    if not asset:
        raise HTTPException(404, "Asset not found")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(asset, k, v)
    await db.flush()
    await db.refresh(asset)
    db.add(ActivityLog(user_id=current_user.id, action="UPDATE", resource_type="asset", resource_id=str(asset.id)))
    return asset


@router.delete("/{asset_id}", status_code=204)
async def delete_asset(
    asset_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    asset = (await db.execute(select(Asset).where(Asset.id == asset_id))).scalar_one_or_none()
    if not asset:
        raise HTTPException(404, "Asset not found")
    db.add(ActivityLog(user_id=current_user.id, action="DELETE", resource_type="asset", resource_id=str(asset.id)))
    await db.delete(asset)


@router.post("/{asset_id}/risks/{risk_id}", status_code=201)
async def link_risk(
    asset_id: UUID,
    risk_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    asset = (await db.execute(select(Asset).where(Asset.id == asset_id))).scalar_one_or_none()
    if not asset:
        raise HTTPException(404, "Asset not found")
    risk = (await db.execute(select(Risk).where(Risk.id == risk_id))).scalar_one_or_none()
    if not risk:
        raise HTTPException(404, "Risk not found")
    existing = (await db.execute(select(AssetRisk).where(AssetRisk.asset_id == asset_id, AssetRisk.risk_id == risk_id))).scalar_one_or_none()
    if existing:
        raise HTTPException(409, "Risk already linked")
    db.add(AssetRisk(asset_id=asset_id, risk_id=risk_id))
    return {"detail": "Risk linked"}


@router.delete("/{asset_id}/risks/{risk_id}", status_code=204)
async def unlink_risk(
    asset_id: UUID,
    risk_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    link = (await db.execute(select(AssetRisk).where(AssetRisk.asset_id == asset_id, AssetRisk.risk_id == risk_id))).scalar_one_or_none()
    if not link:
        raise HTTPException(404, "Link not found")
    await db.delete(link)
