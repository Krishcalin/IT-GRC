"""Monitoring metrics (Clause 9.1, KPI/KRI/KCI) routes."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime, timezone

from ..database import get_db
from ..models.metric import Metric, MetricMeasurement
from ..models.user import User
from ..models.activity_log import ActivityLog
from ..schemas.metric import MetricCreate, MetricUpdate, MetricRead, MeasurementCreate, MeasurementRead
from .deps import get_current_user

router = APIRouter()


@router.get("/", response_model=list[MetricRead])
async def list_metrics(
    metric_type: str | None = None,
    objective_id: UUID | None = None,
    search: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(200, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    q = select(Metric)
    if metric_type:
        q = q.where(Metric.metric_type == metric_type)
    if objective_id:
        q = q.where(Metric.objective_id == objective_id)
    if search:
        q = q.where(or_(Metric.ref_id.ilike(f"%{search}%"), Metric.name.ilike(f"%{search}%")))
    q = q.order_by(Metric.ref_id).offset(skip).limit(limit)
    return (await db.execute(q)).scalars().all()


@router.post("/", response_model=MetricRead, status_code=201)
async def create_metric(
    body: MetricCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    count = (await db.execute(select(func.count()).select_from(Metric))).scalar() or 0
    ref_id = f"MET-{count + 1:03d}"
    metric = Metric(**body.model_dump(), ref_id=ref_id)
    db.add(metric)
    await db.flush()
    await db.refresh(metric)
    db.add(ActivityLog(user_id=current_user.id, action="CREATE", resource_type="metric", resource_id=str(metric.id)))
    return metric


@router.get("/{metric_id}", response_model=MetricRead)
async def get_metric(metric_id: UUID, db: AsyncSession = Depends(get_db)):
    metric = (await db.execute(select(Metric).where(Metric.id == metric_id))).scalar_one_or_none()
    if not metric:
        raise HTTPException(404, "Metric not found")
    return metric


@router.put("/{metric_id}", response_model=MetricRead)
async def update_metric(
    metric_id: UUID,
    body: MetricUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    metric = (await db.execute(select(Metric).where(Metric.id == metric_id))).scalar_one_or_none()
    if not metric:
        raise HTTPException(404, "Metric not found")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(metric, k, v)
    await db.flush()
    await db.refresh(metric)
    db.add(ActivityLog(user_id=current_user.id, action="UPDATE", resource_type="metric", resource_id=str(metric.id)))
    return metric


@router.get("/{metric_id}/history", response_model=list[MeasurementRead])
async def get_metric_history(metric_id: UUID, db: AsyncSession = Depends(get_db)):
    metric = (await db.execute(select(Metric).where(Metric.id == metric_id))).scalar_one_or_none()
    if not metric:
        raise HTTPException(404, "Metric not found")
    rows = (await db.execute(
        select(MetricMeasurement)
        .where(MetricMeasurement.metric_id == metric_id)
        .order_by(MetricMeasurement.captured_at)
    )).scalars().all()
    return rows


@router.post("/{metric_id}/measurements", response_model=MeasurementRead, status_code=201)
async def add_measurement(
    metric_id: UUID,
    body: MeasurementCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Record a point-in-time measurement and update the metric's current value."""
    metric = (await db.execute(select(Metric).where(Metric.id == metric_id))).scalar_one_or_none()
    if not metric:
        raise HTTPException(404, "Metric not found")
    captured = body.captured_at or datetime.now(timezone.utc).date()
    m = MetricMeasurement(metric_id=metric_id, value=body.value, note=body.note, captured_at=captured)
    db.add(m)
    metric.current_value = body.value
    metric.last_measured = captured
    await db.flush()
    await db.refresh(m)
    db.add(ActivityLog(user_id=current_user.id, action="MEASURE", resource_type="metric", resource_id=str(metric.id)))
    return m


@router.delete("/{metric_id}", status_code=204)
async def delete_metric(
    metric_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    metric = (await db.execute(select(Metric).where(Metric.id == metric_id))).scalar_one_or_none()
    if not metric:
        raise HTTPException(404, "Metric not found")
    db.add(ActivityLog(user_id=current_user.id, action="DELETE", resource_type="metric", resource_id=str(metric.id)))
    await db.delete(metric)
