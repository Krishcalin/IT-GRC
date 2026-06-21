"""Analytics & reporting routes.

Provides the data behind the Analytics page: a 5x5 risk heat map, a posture
score trend (compliance / conformity / readiness / training over time), and a
personal "My Work" summary. Posture snapshots are recorded once per day; the
dashboard triggers the daily capture so the trend grows with no scheduler.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models.risk import Risk, _risk_level
from ..models.control import Control
from ..models.clause_requirement import ClauseRequirement
from ..models.documented_information import DocumentedInformation
from ..models.training import TrainingRecord
from ..models.audit import AuditFinding
from ..models.soa import SoAEntry
from ..models.task import Task, task_is_overdue, TASK_OPEN_STATUSES
from ..models.posture import PostureSnapshot
from ..models.user import User
from ..schemas.analytics import RiskHeatmap, HeatCell, PostureSnapshotRead, MyWork
from .deps import get_current_user

router = APIRouter()


async def _count(db: AsyncSession, model, *where) -> int:
    q = select(func.count()).select_from(model)
    for w in where:
        q = q.where(w)
    return (await db.execute(q)).scalar() or 0


async def compute_headline(db: AsyncSession) -> dict:
    """Compute the headline posture numbers used by snapshots (single source of truth)."""
    total_controls = await _count(db, Control)
    implemented = await _count(db, Control, Control.status == "Implemented")

    total_applicable = await _count(db, SoAEntry, SoAEntry.applicable == True)
    fully = await _count(db, SoAEntry, SoAEntry.applicable == True, SoAEntry.implementation_status == "Fully Implemented")
    compliance = round((fully / total_applicable * 100) if total_applicable else (implemented / total_controls * 100) if total_controls else 0, 1)

    total_clauses = await _count(db, ClauseRequirement)
    conformant = await _count(db, ClauseRequirement, ClauseRequirement.conformity_status == "Conformant")
    conformity = round((conformant / total_clauses * 100) if total_clauses else 0, 1)

    mandatory = await _count(db, DocumentedInformation, DocumentedInformation.mandatory == True)
    approved = await _count(db, DocumentedInformation, DocumentedInformation.mandatory == True, DocumentedInformation.status == "Approved")
    readiness = round((approved / mandatory * 100) if mandatory else 0, 1)

    total_records = await _count(db, TrainingRecord)
    completed = await _count(db, TrainingRecord, TrainingRecord.status == "Completed")
    training = round((completed / total_records * 100) if total_records else 0, 1)

    open_risks = await _count(db, Risk, Risk.status.in_(["Open", "In Treatment"]))
    critical_risks = await _count(db, Risk, Risk.inherent_risk_level == "Critical")
    open_findings = await _count(db, AuditFinding, AuditFinding.status.in_(["Open", "In Progress"]))

    tasks = (await db.execute(select(Task))).scalars().all()
    open_tasks = sum(1 for t in tasks if t.status in TASK_OPEN_STATUSES)
    overdue_tasks = sum(1 for t in tasks if task_is_overdue(t.due_date, t.status))

    return {
        "compliance_score": compliance,
        "isms_conformity_score": conformity,
        "document_readiness_score": readiness,
        "training_completion_rate": training,
        "implemented_controls": implemented,
        "total_controls": total_controls,
        "open_risks": open_risks,
        "critical_risks": critical_risks,
        "open_findings": open_findings,
        "open_tasks": open_tasks,
        "overdue_tasks": overdue_tasks,
    }


async def record_posture_snapshot(db: AsyncSession, headline: dict) -> PostureSnapshot:
    """Upsert today's posture snapshot from headline numbers."""
    today = datetime.now(timezone.utc).date()
    snap = (await db.execute(
        select(PostureSnapshot).where(PostureSnapshot.snapshot_date == today)
    )).scalar_one_or_none()
    if snap is None:
        snap = PostureSnapshot(snapshot_date=today)
        db.add(snap)
    for k, v in headline.items():
        setattr(snap, k, v)
    await db.flush()
    return snap


@router.get("/risk-heatmap", response_model=RiskHeatmap)
async def risk_heatmap(
    basis: str = Query("inherent", pattern="^(inherent|residual)$"),
    db: AsyncSession = Depends(get_db),
):
    risks = (await db.execute(select(Risk))).scalars().all()
    counts: dict[tuple[int, int], int] = {}
    for r in risks:
        if basis == "residual" and r.residual_likelihood and r.residual_impact:
            lk, im = r.residual_likelihood, r.residual_impact
        else:
            lk, im = r.likelihood, r.impact
        counts[(lk, im)] = counts.get((lk, im), 0) + 1
    cells: list[HeatCell] = []
    total = 0
    for lk in range(1, 6):
        for im in range(1, 6):
            c = counts.get((lk, im), 0)
            total += c
            cells.append(HeatCell(likelihood=lk, impact=im, score=lk * im, level=_risk_level(lk, im), count=c))
    return RiskHeatmap(basis=basis, cells=cells, total=total)


@router.get("/posture-trend", response_model=list[PostureSnapshotRead])
async def posture_trend(
    days: int = Query(180, ge=1, le=1095),
    db: AsyncSession = Depends(get_db),
):
    cutoff = datetime.now(timezone.utc).date() - timedelta(days=days)
    rows = (await db.execute(
        select(PostureSnapshot)
        .where(PostureSnapshot.snapshot_date >= cutoff)
        .order_by(PostureSnapshot.snapshot_date)
    )).scalars().all()
    return rows


@router.post("/snapshot", response_model=PostureSnapshotRead)
async def capture_snapshot(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    headline = await compute_headline(db)
    return await record_posture_snapshot(db, headline)


@router.get("/my-work", response_model=MyWork)
async def my_work(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tasks = (await db.execute(
        select(Task).where(Task.assignee_id == current_user.id)
    )).scalars().all()
    return MyWork(
        open_tasks=sum(1 for t in tasks if t.status in TASK_OPEN_STATUSES),
        overdue_tasks=sum(1 for t in tasks if task_is_overdue(t.due_date, t.status)),
        pending_approvals=sum(1 for t in tasks if t.task_type == "Approval" and t.status in TASK_OPEN_STATUSES),
        owned_controls=await _count(db, Control, Control.owner_id == current_user.id),
        owned_risks=await _count(db, Risk, Risk.owner_id == current_user.id),
        assigned_findings=await _count(db, AuditFinding, AuditFinding.assigned_to == current_user.id),
    )
