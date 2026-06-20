"""Information security objective (Clause 6.2) schemas."""

from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from .user import UserRead
from .metric import MetricRead


class ObjectiveCreate(BaseModel):
    title: str
    description: str | None = None
    clause_ref: str = "6.2"
    measure: str | None = None
    target_value: str | None = None
    current_value: str | None = None
    unit: str | None = None
    status: str = "Not Started"
    owner_id: UUID | None = None


class ObjectiveUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    measure: str | None = None
    target_value: str | None = None
    current_value: str | None = None
    unit: str | None = None
    status: str | None = None
    owner_id: UUID | None = None
    due_date: date | None = None
    review_date: date | None = None


class ObjectiveRead(BaseModel):
    id: UUID
    ref_id: str
    title: str
    description: str | None = None
    clause_ref: str
    measure: str | None = None
    target_value: str | None = None
    current_value: str | None = None
    unit: str | None = None
    status: str
    owner_id: UUID | None = None
    owner: UserRead | None = None
    due_date: date | None = None
    review_date: date | None = None
    metrics: list[MetricRead] = []
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
