"""Assessment & questionnaire routes — control self-assessments, maturity
assessments, and vendor security questionnaires (campaign + items)."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models.assessment import Assessment, AssessmentItem
from ..models.control import Control
from ..models.user import User
from ..models.activity_log import ActivityLog
from ..schemas.assessment import (
    AssessmentCreate, AssessmentUpdate, AssessmentRead, AssessmentSummary,
    AssessmentItemCreate, AssessmentItemUpdate, AssessmentItemRead,
)
from .deps import get_current_user

router = APIRouter()


async def _get(db: AsyncSession, assessment_id: UUID) -> Assessment:
    a = (await db.execute(select(Assessment).where(Assessment.id == assessment_id))).scalar_one_or_none()
    if not a:
        raise HTTPException(404, "Assessment not found")
    return a


# ── Assessments ───────────────────────────────────────────
@router.get("/", response_model=list[AssessmentSummary])
async def list_assessments(
    assessment_type: str | None = None,
    status: str | None = None,
    search: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(200, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    q = select(Assessment)
    if assessment_type:
        q = q.where(Assessment.assessment_type == assessment_type)
    if status:
        q = q.where(Assessment.status == status)
    if search:
        q = q.where(or_(Assessment.ref_id.ilike(f"%{search}%"), Assessment.title.ilike(f"%{search}%")))
    q = q.order_by(Assessment.ref_id).offset(skip).limit(limit)
    return (await db.execute(q)).scalars().all()


@router.post("/", response_model=AssessmentRead, status_code=201)
async def create_assessment(
    body: AssessmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    count = (await db.execute(select(func.count()).select_from(Assessment))).scalar() or 0
    a = Assessment(**body.model_dump(), ref_id=f"ASMT-{count + 1:03d}")
    db.add(a)
    await db.flush()
    await db.refresh(a)
    db.add(ActivityLog(user_id=current_user.id, action="CREATE", resource_type="assessment", resource_id=str(a.id)))
    return a


@router.get("/{assessment_id}", response_model=AssessmentRead)
async def get_assessment(assessment_id: UUID, db: AsyncSession = Depends(get_db)):
    return await _get(db, assessment_id)


@router.put("/{assessment_id}", response_model=AssessmentRead)
async def update_assessment(
    assessment_id: UUID,
    body: AssessmentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    a = await _get(db, assessment_id)
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(a, k, v)
    await db.flush()
    await db.refresh(a)
    db.add(ActivityLog(user_id=current_user.id, action="UPDATE", resource_type="assessment", resource_id=str(a.id)))
    return a


@router.delete("/{assessment_id}", status_code=204)
async def delete_assessment(
    assessment_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    a = await _get(db, assessment_id)
    db.add(ActivityLog(user_id=current_user.id, action="DELETE", resource_type="assessment", resource_id=str(a.id)))
    await db.delete(a)


@router.post("/{assessment_id}/populate", response_model=AssessmentRead)
async def populate_from_framework(
    assessment_id: UUID,
    framework: str | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create an assessment item for each control in a framework (skips controls already present)."""
    a = await _get(db, assessment_id)
    fw = framework or a.framework
    if not fw:
        raise HTTPException(422, "No framework specified (set assessment.framework or pass ?framework=)")
    controls = (await db.execute(
        select(Control).where(Control.framework == fw).order_by(Control.clause)
    )).scalars().all()
    existing = {i.control_id for i in a.items if i.control_id}
    count = (await db.execute(select(func.count()).select_from(AssessmentItem))).scalar() or 0
    added = 0
    for c in controls:
        if c.id in existing:
            continue
        count += 1
        added += 1
        db.add(AssessmentItem(
            ref_id=f"ASI-{count:03d}", assessment_id=assessment_id, control_id=c.id,
            question=f"{c.clause} — {c.title}",
        ))
    await db.flush()
    db.add(ActivityLog(user_id=current_user.id, action=f"POPULATE:{added}", resource_type="assessment", resource_id=str(a.id)))
    await db.refresh(a)
    return a


# ── Items ─────────────────────────────────────────────────
@router.post("/{assessment_id}/items", response_model=AssessmentItemRead, status_code=201)
async def add_item(
    assessment_id: UUID,
    body: AssessmentItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await _get(db, assessment_id)
    count = (await db.execute(select(func.count()).select_from(AssessmentItem))).scalar() or 0
    item = AssessmentItem(**body.model_dump(), assessment_id=assessment_id, ref_id=f"ASI-{count + 1:03d}")
    db.add(item)
    await db.flush()
    await db.refresh(item)
    db.add(ActivityLog(user_id=current_user.id, action="CREATE", resource_type="assessment_item", resource_id=str(item.id)))
    return item


@router.put("/{assessment_id}/items/{item_id}", response_model=AssessmentItemRead)
async def update_item(
    assessment_id: UUID,
    item_id: UUID,
    body: AssessmentItemUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = (await db.execute(
        select(AssessmentItem).where(AssessmentItem.id == item_id, AssessmentItem.assessment_id == assessment_id)
    )).scalar_one_or_none()
    if not item:
        raise HTTPException(404, "Assessment item not found")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(item, k, v)
    await db.flush()
    await db.refresh(item)
    db.add(ActivityLog(user_id=current_user.id, action="UPDATE", resource_type="assessment_item", resource_id=str(item.id)))
    return item


@router.delete("/{assessment_id}/items/{item_id}", status_code=204)
async def delete_item(
    assessment_id: UUID,
    item_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = (await db.execute(
        select(AssessmentItem).where(AssessmentItem.id == item_id, AssessmentItem.assessment_id == assessment_id)
    )).scalar_one_or_none()
    if not item:
        raise HTTPException(404, "Assessment item not found")
    db.add(ActivityLog(user_id=current_user.id, action="DELETE", resource_type="assessment_item", resource_id=str(item.id)))
    await db.delete(item)
