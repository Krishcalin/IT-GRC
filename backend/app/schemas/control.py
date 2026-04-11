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
    implementation_guidance: str | None = None
    status: str
    owner_id: UUID | None = None
    owner: UserRead | None = None
    review_date: date | None = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
