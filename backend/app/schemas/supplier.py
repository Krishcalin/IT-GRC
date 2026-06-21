"""Supplier / third-party (Clauses 5.19–5.23) schemas."""

from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from .user import UserRead


class SupplierCreate(BaseModel):
    name: str
    description: str | None = None
    category: str = "Service"
    service_description: str | None = None
    criticality: str = "Medium"
    data_classification: str = "Internal"
    status: str = "Active"
    is_requirements_agreed: bool = False
    right_to_audit: bool = False
    processes_pii: bool = False
    certifications: str | None = None
    owner_id: UUID | None = None
    contract_start: date | None = None
    contract_end: date | None = None
    next_review_date: date | None = None
    notes: str | None = None


class SupplierUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    category: str | None = None
    service_description: str | None = None
    criticality: str | None = None
    data_classification: str | None = None
    status: str | None = None
    is_requirements_agreed: bool | None = None
    right_to_audit: bool | None = None
    processes_pii: bool | None = None
    certifications: str | None = None
    owner_id: UUID | None = None
    contract_start: date | None = None
    contract_end: date | None = None
    last_review_date: date | None = None
    next_review_date: date | None = None
    notes: str | None = None


class SupplierRead(BaseModel):
    id: UUID
    ref_id: str
    name: str
    description: str | None = None
    category: str
    service_description: str | None = None
    criticality: str
    data_classification: str
    status: str
    is_requirements_agreed: bool
    right_to_audit: bool
    processes_pii: bool
    certifications: str | None = None
    owner_id: UUID | None = None
    owner: UserRead | None = None
    contract_start: date | None = None
    contract_end: date | None = None
    last_review_date: date | None = None
    next_review_date: date | None = None
    notes: str | None = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
