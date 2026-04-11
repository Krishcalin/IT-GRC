"""Statement of Applicability schemas."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from .control import ControlRead
from .user import UserRead


class SoACreate(BaseModel):
    control_id: UUID
    applicable: bool = True
    justification: str | None = None
    implementation_status: str = "Not Implemented"
    implementation_evidence: str | None = None
    responsible_id: UUID | None = None
    notes: str | None = None


class SoAUpdate(BaseModel):
    applicable: bool | None = None
    justification: str | None = None
    implementation_status: str | None = None
    implementation_evidence: str | None = None
    responsible_id: UUID | None = None
    notes: str | None = None


class SoARead(BaseModel):
    id: UUID
    control_id: UUID
    applicable: bool
    justification: str | None = None
    implementation_status: str
    implementation_evidence: str | None = None
    responsible_id: UUID | None = None
    responsible: UserRead | None = None
    notes: str | None = None
    control: ControlRead
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
