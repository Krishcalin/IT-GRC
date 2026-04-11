"""Audit and AuditFinding routes."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models.audit import Audit, AuditFinding
from ..models.user import User
from ..models.activity_log import ActivityLog
from ..schemas.audit import (
    AuditCreate, AuditUpdate, AuditRead,
    AuditFindingCreate, AuditFindingUpdate, AuditFindingRead,
)
from .deps import get_current_user

router = APIRouter()


@router.get("/", response_model=list[AuditRead])
async def list_audits(
    status: str | None = None,
    audit_type: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    q = select(Audit)
    if status:
        q = q.where(Audit.status == status)
    if audit_type:
        q = q.where(Audit.audit_type == audit_type)
    q = q.order_by(Audit.ref_id).offset(skip).limit(limit)
    return (await db.execute(q)).scalars().all()


@router.post("/", response_model=AuditRead, status_code=201)
async def create_audit(
    body: AuditCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    count = (await db.execute(select(func.count()).select_from(Audit))).scalar() or 0
    ref_id = f"AUDIT-{count + 1:03d}"
    audit = Audit(**body.model_dump(), ref_id=ref_id)
    db.add(audit)
    await db.flush()
    await db.refresh(audit)
    db.add(ActivityLog(user_id=current_user.id, action="CREATE", resource_type="audit", resource_id=str(audit.id)))
    return audit


@router.get("/{audit_id}", response_model=AuditRead)
async def get_audit(audit_id: UUID, db: AsyncSession = Depends(get_db)):
    audit = (await db.execute(select(Audit).where(Audit.id == audit_id))).scalar_one_or_none()
    if not audit:
        raise HTTPException(404, "Audit not found")
    return audit


@router.put("/{audit_id}", response_model=AuditRead)
async def update_audit(
    audit_id: UUID,
    body: AuditUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    audit = (await db.execute(select(Audit).where(Audit.id == audit_id))).scalar_one_or_none()
    if not audit:
        raise HTTPException(404, "Audit not found")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(audit, k, v)
    await db.flush()
    await db.refresh(audit)
    db.add(ActivityLog(user_id=current_user.id, action="UPDATE", resource_type="audit", resource_id=str(audit.id)))
    return audit


@router.delete("/{audit_id}", status_code=204)
async def delete_audit(
    audit_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    audit = (await db.execute(select(Audit).where(Audit.id == audit_id))).scalar_one_or_none()
    if not audit:
        raise HTTPException(404, "Audit not found")
    db.add(ActivityLog(user_id=current_user.id, action="DELETE", resource_type="audit", resource_id=str(audit.id)))
    await db.delete(audit)


# ── Findings ──────────────────────────────────────────────

@router.post("/{audit_id}/findings", response_model=AuditFindingRead, status_code=201)
async def create_finding(
    audit_id: UUID,
    body: AuditFindingCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    audit = (await db.execute(select(Audit).where(Audit.id == audit_id))).scalar_one_or_none()
    if not audit:
        raise HTTPException(404, "Audit not found")

    count = (await db.execute(select(func.count()).select_from(AuditFinding))).scalar() or 0
    ref_id = f"FIND-{count + 1:03d}"
    finding = AuditFinding(**body.model_dump(exclude={"audit_id"}), audit_id=audit_id, ref_id=ref_id)
    db.add(finding)
    await db.flush()
    await db.refresh(finding)
    db.add(ActivityLog(user_id=current_user.id, action="CREATE", resource_type="audit_finding", resource_id=str(finding.id)))
    return finding


@router.put("/findings/{finding_id}", response_model=AuditFindingRead)
async def update_finding(
    finding_id: UUID,
    body: AuditFindingUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    finding = (await db.execute(select(AuditFinding).where(AuditFinding.id == finding_id))).scalar_one_or_none()
    if not finding:
        raise HTTPException(404, "Finding not found")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(finding, k, v)
    await db.flush()
    await db.refresh(finding)
    db.add(ActivityLog(user_id=current_user.id, action="UPDATE", resource_type="audit_finding", resource_id=str(finding.id)))
    return finding


@router.delete("/findings/{finding_id}", status_code=204)
async def delete_finding(
    finding_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    finding = (await db.execute(select(AuditFinding).where(AuditFinding.id == finding_id))).scalar_one_or_none()
    if not finding:
        raise HTTPException(404, "Finding not found")
    db.add(ActivityLog(user_id=current_user.id, action="DELETE", resource_type="audit_finding", resource_id=str(finding.id)))
    await db.delete(finding)
