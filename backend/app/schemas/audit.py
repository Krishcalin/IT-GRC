"""Audit and AuditFinding schemas."""

from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from .control import ControlRead
from .user import UserRead


class AuditFindingCreate(BaseModel):
    audit_id: UUID
    control_id: UUID | None = None
    finding_type: str
    description: str
    severity: str = "Medium"
    corrective_action: str | None = None
    due_date: date | None = None
    assigned_to: UUID | None = None


class AuditFindingUpdate(BaseModel):
    finding_type: str | None = None
    description: str | None = None
    severity: str | None = None
    corrective_action: str | None = None
    due_date: date | None = None
    status: str | None = None
    assigned_to: UUID | None = None


class AuditFindingRead(BaseModel):
    id: UUID
    ref_id: str
    audit_id: UUID
    control_id: UUID | None = None
    control: ControlRead | None = None
    finding_type: str
    description: str
    severity: str
    corrective_action: str | None = None
    due_date: date | None = None
    status: str
    assigned_to: UUID | None = None
    assignee: UserRead | None = None
    closed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class AuditCreate(BaseModel):
    title: str
    description: str | None = None
    audit_type: str
    lead_auditor_id: UUID | None = None
    start_date: date | None = None
    end_date: date | None = None
    scope: str | None = None


class AuditUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    audit_type: str | None = None
    status: str | None = None
    lead_auditor_id: UUID | None = None
    start_date: date | None = None
    end_date: date | None = None
    scope: str | None = None
    conclusion: str | None = None


class AuditRead(BaseModel):
    id: UUID
    ref_id: str
    title: str
    description: str | None = None
    audit_type: str
    status: str
    lead_auditor_id: UUID | None = None
    lead_auditor: UserRead | None = None
    start_date: date | None = None
    end_date: date | None = None
    scope: str | None = None
    conclusion: str | None = None
    findings: list[AuditFindingRead] = []
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
