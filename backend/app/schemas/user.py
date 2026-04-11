"""User and Role schemas."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class RoleRead(BaseModel):
    id: UUID
    name: str
    description: str | None = None
    permissions: list | None = None
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    department: str | None = None
    is_superuser: bool = False


class UserUpdate(BaseModel):
    full_name: str | None = None
    department: str | None = None
    is_active: bool | None = None


class UserRead(BaseModel):
    id: UUID
    email: str
    full_name: str
    department: str | None = None
    is_active: bool
    is_superuser: bool
    auth_provider: str
    roles: list[RoleRead] = []
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
