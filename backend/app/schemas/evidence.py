"""Evidence schemas."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from .user import UserRead


class EvidenceCreate(BaseModel):
    title: str
    description: str | None = None
    control_id: UUID | None = None
    risk_id: UUID | None = None
    audit_id: UUID | None = None
    policy_id: UUID | None = None


class EvidenceRead(BaseModel):
    id: UUID
    title: str
    description: str | None = None
    file_name: str
    file_path: str
    file_type: str | None = None
    file_size: int | None = None
    uploaded_by: UUID | None = None
    uploader: UserRead | None = None
    control_id: UUID | None = None
    risk_id: UUID | None = None
    audit_id: UUID | None = None
    policy_id: UUID | None = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
