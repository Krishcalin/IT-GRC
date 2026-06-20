"""Documented information (Clause 7.5) schemas."""

from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from .user import UserRead


class DocumentCreate(BaseModel):
    title: str
    description: str | None = None
    doc_type: str
    clause_ref: str | None = None
    mandatory: bool = False
    version: str = "0.1"
    status: str = "Draft"
    classification: str = "Internal"
    location: str | None = None
    owner_id: UUID | None = None
    approver_id: UUID | None = None


class DocumentUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    doc_type: str | None = None
    clause_ref: str | None = None
    mandatory: bool | None = None
    version: str | None = None
    status: str | None = None
    classification: str | None = None
    location: str | None = None
    owner_id: UUID | None = None
    approver_id: UUID | None = None
    approved_at: datetime | None = None
    review_date: date | None = None
    next_review_date: date | None = None


class DocumentRead(BaseModel):
    id: UUID
    ref_id: str
    title: str
    description: str | None = None
    doc_type: str
    clause_ref: str | None = None
    mandatory: bool
    version: str
    status: str
    classification: str
    location: str | None = None
    owner_id: UUID | None = None
    owner: UserRead | None = None
    approver_id: UUID | None = None
    approver: UserRead | None = None
    approved_at: datetime | None = None
    review_date: date | None = None
    next_review_date: date | None = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
