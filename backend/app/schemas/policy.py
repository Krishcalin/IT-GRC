"""Policy schemas."""

from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from .user import UserRead


class PolicyAckRead(BaseModel):
    id: UUID
    user: UserRead
    acknowledged_at: datetime
    model_config = ConfigDict(from_attributes=True)


class PolicyCreate(BaseModel):
    title: str
    description: str | None = None
    category: str
    content: str | None = None
    owner_id: UUID | None = None


class PolicyUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    version: str | None = None
    status: str | None = None
    category: str | None = None
    owner_id: UUID | None = None
    approved_by: UUID | None = None
    effective_date: date | None = None
    review_date: date | None = None
    next_review_date: date | None = None
    content: str | None = None


class PolicyRead(BaseModel):
    id: UUID
    ref_id: str
    title: str
    description: str | None = None
    version: str
    status: str
    category: str
    owner_id: UUID | None = None
    owner: UserRead | None = None
    approved_by: UUID | None = None
    approver: UserRead | None = None
    approved_at: datetime | None = None
    effective_date: date | None = None
    review_date: date | None = None
    next_review_date: date | None = None
    content: str | None = None
    acknowledgments: list[PolicyAckRead] = []
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
