"""Assessment & questionnaire schemas."""

from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from .user import UserRead
from .control import ControlSummary


class AssessmentItemCreate(BaseModel):
    control_id: UUID | None = None
    question: str | None = None
    response: str | None = None
    maturity: int | None = None
    result: str | None = None
    comment: str | None = None


class AssessmentItemUpdate(BaseModel):
    question: str | None = None
    response: str | None = None
    maturity: int | None = None
    result: str | None = None
    comment: str | None = None


class AssessmentItemRead(BaseModel):
    id: UUID
    ref_id: str
    assessment_id: UUID
    control_id: UUID | None = None
    control: ControlSummary | None = None
    question: str | None = None
    response: str | None = None
    maturity: int | None = None
    result: str | None = None
    comment: str | None = None
    model_config = ConfigDict(from_attributes=True)


class AssessmentCreate(BaseModel):
    title: str
    description: str | None = None
    assessment_type: str = "Control Self-Assessment"
    framework: str | None = None
    supplier_id: UUID | None = None
    owner_id: UUID | None = None
    status: str = "Draft"
    due_date: date | None = None


class AssessmentUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    assessment_type: str | None = None
    framework: str | None = None
    supplier_id: UUID | None = None
    owner_id: UUID | None = None
    status: str | None = None
    due_date: date | None = None


class AssessmentRead(BaseModel):
    id: UUID
    ref_id: str
    title: str
    description: str | None = None
    assessment_type: str
    framework: str | None = None
    supplier_id: UUID | None = None
    owner_id: UUID | None = None
    owner: UserRead | None = None
    status: str
    due_date: date | None = None
    item_count: int = 0
    answered_count: int = 0
    avg_maturity: float | None = None
    score: float = 0.0
    items: list[AssessmentItemRead] = []
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class AssessmentSummary(BaseModel):
    """Assessment without items — for list views."""
    id: UUID
    ref_id: str
    title: str
    assessment_type: str
    framework: str | None = None
    status: str
    owner: UserRead | None = None
    due_date: date | None = None
    item_count: int = 0
    answered_count: int = 0
    score: float = 0.0
    model_config = ConfigDict(from_attributes=True)
