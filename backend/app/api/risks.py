"""Risk Register routes."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models.risk import Risk, RiskControl
from ..models.control import Control
from ..models.user import User
from ..models.activity_log import ActivityLog
from ..schemas.risk import RiskCreate, RiskUpdate, RiskRead
from .deps import get_current_user

router = APIRouter()


def _risk_level(likelihood: int, impact: int) -> str:
    score = likelihood * impact
    if score >= 20:
        return "Critical"
    if score >= 12:
        return "High"
    if score >= 6:
        return "Medium"
    return "Low"


@router.get("/", response_model=list[RiskRead])
async def list_risks(
    category: str | None = None,
    status: str | None = None,
    risk_level: str | None = None,
    search: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    q = select(Risk)
    if category:
        q = q.where(Risk.category == category)
    if status:
        q = q.where(Risk.status == status)
    if risk_level:
        q = q.where(Risk.inherent_risk_level == risk_level)
    if search:
        q = q.where(or_(Risk.ref_id.ilike(f"%{search}%"), Risk.title.ilike(f"%{search}%")))
    q = q.order_by(Risk.ref_id).offset(skip).limit(limit)
    return (await db.execute(q)).scalars().all()


@router.post("/", response_model=RiskRead, status_code=201)
async def create_risk(
    body: RiskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    count = (await db.execute(select(func.count()).select_from(Risk))).scalar() or 0
    ref_id = f"RISK-{count + 1:03d}"
    level = _risk_level(body.likelihood, body.impact)
    risk = Risk(**body.model_dump(), ref_id=ref_id, inherent_risk_level=level)
    db.add(risk)
    await db.flush()
    await db.refresh(risk)
    db.add(ActivityLog(user_id=current_user.id, action="CREATE", resource_type="risk", resource_id=str(risk.id)))
    return risk


@router.get("/{risk_id}", response_model=RiskRead)
async def get_risk(risk_id: UUID, db: AsyncSession = Depends(get_db)):
    risk = (await db.execute(select(Risk).where(Risk.id == risk_id))).scalar_one_or_none()
    if not risk:
        raise HTTPException(404, "Risk not found")
    return risk


@router.put("/{risk_id}", response_model=RiskRead)
async def update_risk(
    risk_id: UUID,
    body: RiskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    risk = (await db.execute(select(Risk).where(Risk.id == risk_id))).scalar_one_or_none()
    if not risk:
        raise HTTPException(404, "Risk not found")

    data = body.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(risk, k, v)

    # Recompute inherent risk level
    lk = data.get("likelihood", risk.likelihood)
    im = data.get("impact", risk.impact)
    risk.inherent_risk_level = _risk_level(lk, im)

    # Recompute residual risk level if provided
    rl = data.get("residual_likelihood", risk.residual_likelihood)
    ri = data.get("residual_impact", risk.residual_impact)
    if rl is not None and ri is not None:
        risk.residual_risk_level = _risk_level(rl, ri)

    await db.flush()
    await db.refresh(risk)
    db.add(ActivityLog(user_id=current_user.id, action="UPDATE", resource_type="risk", resource_id=str(risk.id)))
    return risk


@router.delete("/{risk_id}", status_code=204)
async def delete_risk(
    risk_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    risk = (await db.execute(select(Risk).where(Risk.id == risk_id))).scalar_one_or_none()
    if not risk:
        raise HTTPException(404, "Risk not found")
    db.add(ActivityLog(user_id=current_user.id, action="DELETE", resource_type="risk", resource_id=str(risk.id)))
    await db.delete(risk)


@router.post("/{risk_id}/controls/{control_id}", status_code=201)
async def link_control(
    risk_id: UUID,
    control_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    risk = (await db.execute(select(Risk).where(Risk.id == risk_id))).scalar_one_or_none()
    if not risk:
        raise HTTPException(404, "Risk not found")
    ctrl = (await db.execute(select(Control).where(Control.id == control_id))).scalar_one_or_none()
    if not ctrl:
        raise HTTPException(404, "Control not found")
    existing = (await db.execute(select(RiskControl).where(RiskControl.risk_id == risk_id, RiskControl.control_id == control_id))).scalar_one_or_none()
    if existing:
        raise HTTPException(409, "Control already linked")
    db.add(RiskControl(risk_id=risk_id, control_id=control_id))
    return {"detail": "Control linked"}


@router.delete("/{risk_id}/controls/{control_id}", status_code=204)
async def unlink_control(
    risk_id: UUID,
    control_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    link = (await db.execute(select(RiskControl).where(RiskControl.risk_id == risk_id, RiskControl.control_id == control_id))).scalar_one_or_none()
    if not link:
        raise HTTPException(404, "Link not found")
    await db.delete(link)
