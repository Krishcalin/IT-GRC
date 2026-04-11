"""Evidence management routes."""

from __future__ import annotations

import os
import uuid as _uuid
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import settings
from ..database import get_db
from ..models.evidence import Evidence
from ..models.user import User
from ..models.activity_log import ActivityLog
from ..schemas.evidence import EvidenceRead
from .deps import get_current_user

router = APIRouter()


@router.get("/", response_model=list[EvidenceRead])
async def list_evidence(
    control_id: UUID | None = None,
    risk_id: UUID | None = None,
    audit_id: UUID | None = None,
    policy_id: UUID | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    q = select(Evidence)
    if control_id:
        q = q.where(Evidence.control_id == control_id)
    if risk_id:
        q = q.where(Evidence.risk_id == risk_id)
    if audit_id:
        q = q.where(Evidence.audit_id == audit_id)
    if policy_id:
        q = q.where(Evidence.policy_id == policy_id)
    q = q.order_by(Evidence.created_at.desc()).offset(skip).limit(limit)
    return (await db.execute(q)).scalars().all()


@router.post("/upload", response_model=EvidenceRead, status_code=201)
async def upload_evidence(
    title: str = Form(...),
    description: str | None = Form(None),
    control_id: UUID | None = Form(None),
    risk_id: UUID | None = Form(None),
    audit_id: UUID | None = Form(None),
    policy_id: UUID | None = Form(None),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Validate file size
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    content = await file.read()
    if len(content) > max_bytes:
        raise HTTPException(413, f"File exceeds {settings.MAX_UPLOAD_SIZE_MB} MB limit")

    # Save file
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    ext = os.path.splitext(file.filename or "file")[1]
    safe_name = f"{_uuid.uuid4().hex}{ext}"
    file_path = os.path.join(settings.UPLOAD_DIR, safe_name)
    with open(file_path, "wb") as f:
        f.write(content)

    evidence = Evidence(
        title=title,
        description=description,
        file_name=file.filename or "unknown",
        file_path=file_path,
        file_type=file.content_type,
        file_size=len(content),
        uploaded_by=current_user.id,
        control_id=control_id,
        risk_id=risk_id,
        audit_id=audit_id,
        policy_id=policy_id,
    )
    db.add(evidence)
    await db.flush()
    await db.refresh(evidence)
    db.add(ActivityLog(user_id=current_user.id, action="CREATE", resource_type="evidence", resource_id=str(evidence.id)))
    return evidence


@router.get("/{evidence_id}", response_model=EvidenceRead)
async def get_evidence(evidence_id: UUID, db: AsyncSession = Depends(get_db)):
    ev = (await db.execute(select(Evidence).where(Evidence.id == evidence_id))).scalar_one_or_none()
    if not ev:
        raise HTTPException(404, "Evidence not found")
    return ev


@router.get("/{evidence_id}/download")
async def download_evidence(evidence_id: UUID, db: AsyncSession = Depends(get_db)):
    ev = (await db.execute(select(Evidence).where(Evidence.id == evidence_id))).scalar_one_or_none()
    if not ev:
        raise HTTPException(404, "Evidence not found")
    if not os.path.isfile(ev.file_path):
        raise HTTPException(404, "File not found on disk")
    return FileResponse(ev.file_path, filename=ev.file_name, media_type=ev.file_type or "application/octet-stream")


@router.delete("/{evidence_id}", status_code=204)
async def delete_evidence(
    evidence_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ev = (await db.execute(select(Evidence).where(Evidence.id == evidence_id))).scalar_one_or_none()
    if not ev:
        raise HTTPException(404, "Evidence not found")
    if os.path.isfile(ev.file_path):
        os.remove(ev.file_path)
    db.add(ActivityLog(user_id=current_user.id, action="DELETE", resource_type="evidence", resource_id=str(ev.id)))
    await db.delete(ev)
