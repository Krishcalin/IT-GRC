"""Interested parties (Clause 4.2) schemas."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from .user import UserRead


class InterestedPartyCreate(BaseModel):
    name: str
    party_type: str = "External"
    category: str
    requirements: str | None = None
    addressed_in_isms: bool = False
    notes: str | None = None
    owner_id: UUID | None = None


class InterestedPartyUpdate(BaseModel):
    name: str | None = None
    party_type: str | None = None
    category: str | None = None
    requirements: str | None = None
    addressed_in_isms: bool | None = None
    notes: str | None = None
    owner_id: UUID | None = None


class InterestedPartyRead(BaseModel):
    id: UUID
    ref_id: str
    name: str
    party_type: str
    category: str
    requirements: str | None = None
    addressed_in_isms: bool
    notes: str | None = None
    owner_id: UUID | None = None
    owner: UserRead | None = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
