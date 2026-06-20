"""Documented information (Clause 7.5) routes."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models.documented_information import DocumentedInformation
from ..models.user import User
from ..models.activity_log import ActivityLog
from ..schemas.documented_information import DocumentCreate, DocumentUpdate, DocumentRead
from .deps import get_current_user, require_superuser

router = APIRouter()


@router.get("/", response_model=list[DocumentRead])
async def list_documents(
    doc_type: str | None = None,
    status: str | None = None,
    mandatory: bool | None = None,
    clause_ref: str | None = None,
    search: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(200, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    q = select(DocumentedInformation)
    if doc_type:
        q = q.where(DocumentedInformation.doc_type == doc_type)
    if status:
        q = q.where(DocumentedInformation.status == status)
    if mandatory is not None:
        q = q.where(DocumentedInformation.mandatory == mandatory)
    if clause_ref:
        q = q.where(DocumentedInformation.clause_ref == clause_ref)
    if search:
        q = q.where(or_(
            DocumentedInformation.ref_id.ilike(f"%{search}%"),
            DocumentedInformation.title.ilike(f"%{search}%"),
        ))
    q = q.order_by(DocumentedInformation.ref_id).offset(skip).limit(limit)
    return (await db.execute(q)).scalars().all()


@router.post("/", response_model=DocumentRead, status_code=201)
async def create_document(
    body: DocumentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    count = (await db.execute(select(func.count()).select_from(DocumentedInformation))).scalar() or 0
    ref_id = f"DOC-{count + 1:03d}"
    doc = DocumentedInformation(**body.model_dump(), ref_id=ref_id)
    db.add(doc)
    await db.flush()
    await db.refresh(doc)
    db.add(ActivityLog(user_id=current_user.id, action="CREATE", resource_type="document", resource_id=str(doc.id)))
    return doc


@router.get("/{doc_id}", response_model=DocumentRead)
async def get_document(doc_id: UUID, db: AsyncSession = Depends(get_db)):
    doc = (await db.execute(select(DocumentedInformation).where(DocumentedInformation.id == doc_id))).scalar_one_or_none()
    if not doc:
        raise HTTPException(404, "Document not found")
    return doc


@router.put("/{doc_id}", response_model=DocumentRead)
async def update_document(
    doc_id: UUID,
    body: DocumentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    doc = (await db.execute(select(DocumentedInformation).where(DocumentedInformation.id == doc_id))).scalar_one_or_none()
    if not doc:
        raise HTTPException(404, "Document not found")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(doc, k, v)
    await db.flush()
    await db.refresh(doc)
    db.add(ActivityLog(user_id=current_user.id, action="UPDATE", resource_type="document", resource_id=str(doc.id)))
    return doc


@router.delete("/{doc_id}", status_code=204)
async def delete_document(
    doc_id: UUID,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_superuser),
):
    doc = (await db.execute(select(DocumentedInformation).where(DocumentedInformation.id == doc_id))).scalar_one_or_none()
    if not doc:
        raise HTTPException(404, "Document not found")
    db.add(ActivityLog(user_id=admin.id, action="DELETE", resource_type="document", resource_id=str(doc.id)))
    await db.delete(doc)
