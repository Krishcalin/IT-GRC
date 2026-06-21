"""Monitoring metric (Clause 9.1, KPI/KRI/KCI) schemas."""

from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from .user import UserRead


class MetricCreate(BaseModel):
    name: str
    description: str | None = None
    metric_type: str = "KPI"
    clause_ref: str = "9.1"
    objective_id: UUID | None = None
    target_value: float | None = None
    current_value: float | None = None
    unit: str | None = None
    direction: str = "higher_is_better"
    frequency: str | None = None
    owner_id: UUID | None = None


class MetricUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    metric_type: str | None = None
    objective_id: UUID | None = None
    target_value: float | None = None
    current_value: float | None = None
    unit: str | None = None
    direction: str | None = None
    frequency: str | None = None
    owner_id: UUID | None = None
    last_measured: date | None = None


class MeasurementCreate(BaseModel):
    value: float
    note: str | None = None
    captured_at: date | None = None


class MeasurementRead(BaseModel):
    id: UUID
    metric_id: UUID
    value: float
    note: str | None = None
    captured_at: date
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class MetricRead(BaseModel):
    id: UUID
    ref_id: str
    name: str
    description: str | None = None
    metric_type: str
    clause_ref: str
    objective_id: UUID | None = None
    target_value: float | None = None
    current_value: float | None = None
    unit: str | None = None
    direction: str
    frequency: str | None = None
    rag: str  # derived from target vs. current (model property)
    owner_id: UUID | None = None
    owner: UserRead | None = None
    last_measured: date | None = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
