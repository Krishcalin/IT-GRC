"""Control schemas."""

from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from .user import UserRead


class ControlCreate(BaseModel):
    clause: str
    title: str
    description: str
    theme: str
    framework: str = "ISO 27001:2022"
    implementation_guidance: str | None = None
    status: str = "Not Started"
    owner_id: UUID | None = None


class ControlUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    theme: str | None = None
    implementation_guidance: str | None = None
    status: str | None = None
    owner_id: UUID | None = None
    review_date: date | None = None


class ControlRead(BaseModel):
    id: UUID
    clause: str
    title: str
    description: str
    theme: str
    framework: str = "ISO 27001:2022"
    implementation_guidance: str | None = None
    status: str
    owner_id: UUID | None = None
    owner: UserRead | None = None
    review_date: date | None = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ControlSummary(BaseModel):
    """Lightweight control reference for crosswalk listings."""
    id: UUID
    clause: str
    title: str
    framework: str
    theme: str
    status: str
    model_config = ConfigDict(from_attributes=True)


class ControlMappingCreate(BaseModel):
    target_control_id: UUID
    relationship_type: str = "related"
    note: str | None = None


class ControlMappingRead(BaseModel):
    id: UUID
    relationship_type: str
    note: str | None = None
    direction: str  # outgoing | incoming
    control: ControlSummary  # the OTHER control in the mapping
