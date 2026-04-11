"""Risk schemas."""

from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from .user import UserRead


class RiskCreate(BaseModel):
    title: str
    description: str
    category: str
    likelihood: int = Field(ge=1, le=5)
    impact: int = Field(ge=1, le=5)
    treatment: str = "Mitigate"
    treatment_plan: str | None = None
    owner_id: UUID | None = None


class RiskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    category: str | None = None
    likelihood: int | None = Field(default=None, ge=1, le=5)
    impact: int | None = Field(default=None, ge=1, le=5)
    treatment: str | None = None
    treatment_plan: str | None = None
    residual_likelihood: int | None = Field(default=None, ge=1, le=5)
    residual_impact: int | None = Field(default=None, ge=1, le=5)
    owner_id: UUID | None = None
    status: str | None = None
    review_date: date | None = None


class RiskRead(BaseModel):
    id: UUID
    ref_id: str
    title: str
    description: str
    category: str
    likelihood: int
    impact: int
    inherent_risk_level: str
    treatment: str
    treatment_plan: str | None = None
    residual_likelihood: int | None = None
    residual_impact: int | None = None
    residual_risk_level: str | None = None
    owner_id: UUID | None = None
    owner: UserRead | None = None
    status: str
    review_date: date | None = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
