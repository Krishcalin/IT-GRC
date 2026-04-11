"""Asset schemas."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from .user import UserRead


class AssetCreate(BaseModel):
    name: str
    description: str | None = None
    asset_type: str
    classification: str = "Internal"
    owner_id: UUID | None = None
    department: str | None = None
    location: str | None = None
    criticality: str = "Medium"


class AssetUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    asset_type: str | None = None
    classification: str | None = None
    owner_id: UUID | None = None
    department: str | None = None
    location: str | None = None
    status: str | None = None
    criticality: str | None = None


class AssetRead(BaseModel):
    id: UUID
    ref_id: str
    name: str
    description: str | None = None
    asset_type: str
    classification: str
    owner_id: UUID | None = None
    owner: UserRead | None = None
    department: str | None = None
    location: str | None = None
    status: str
    criticality: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
