"""Information security incident (Clauses 5.24–5.28) schemas."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from .user import UserRead


class IncidentCreate(BaseModel):
    title: str
    description: str | None = None
    category: str = "Other"
    severity: str = "Medium"
    status: str = "New"
    reporter: str | None = None
    owner_id: UUID | None = None
    risk_id: UUID | None = None
    affected_assets: str | None = None
    data_breach: bool = False


class IncidentUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    category: str | None = None
    severity: str | None = None
    status: str | None = None
    reporter: str | None = None
    owner_id: UUID | None = None
    risk_id: UUID | None = None
    affected_assets: str | None = None
    data_breach: bool | None = None
    containment_actions: str | None = None
    root_cause: str | None = None
    lessons_learned: str | None = None
    evidence_notes: str | None = None
    resolved_at: datetime | None = None


class IncidentRead(BaseModel):
    id: UUID
    ref_id: str
    title: str
    description: str | None = None
    category: str
    severity: str
    status: str
    reporter: str | None = None
    reported_at: datetime
    owner_id: UUID | None = None
    owner: UserRead | None = None
    risk_id: UUID | None = None
    affected_assets: str | None = None
    data_breach: bool
    containment_actions: str | None = None
    root_cause: str | None = None
    lessons_learned: str | None = None
    evidence_notes: str | None = None
    resolved_at: datetime | None = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
