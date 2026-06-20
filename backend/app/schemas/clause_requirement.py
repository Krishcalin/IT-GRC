"""ISMS clause requirement (Clauses 4–10) schemas."""

from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from .user import UserRead


class ClauseRequirementCreate(BaseModel):
    clause: str
    title: str
    section: str
    clause_number: int
    requirement: str
    documented_info: str | None = None
    conformity_status: str = "Not Assessed"
    implementation_notes: str | None = None
    owner_id: UUID | None = None


class ClauseRequirementUpdate(BaseModel):
    title: str | None = None
    section: str | None = None
    requirement: str | None = None
    documented_info: str | None = None
    conformity_status: str | None = None
    implementation_notes: str | None = None
    owner_id: UUID | None = None
    review_date: date | None = None


class ClauseRequirementRead(BaseModel):
    id: UUID
    clause: str
    title: str
    section: str
    clause_number: int
    requirement: str
    documented_info: str | None = None
    conformity_status: str
    implementation_notes: str | None = None
    owner_id: UUID | None = None
    owner: UserRead | None = None
    review_date: date | None = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
