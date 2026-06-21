"""Workflow task & approval schemas."""

from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from .user import UserRead


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    task_type: str = "Action"
    status: str = "Open"
    priority: str = "Medium"
    assignee_id: UUID | None = None
    due_date: date | None = None
    resource_type: str | None = None
    resource_id: str | None = None
    resource_label: str | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    task_type: str | None = None
    status: str | None = None
    priority: str | None = None
    assignee_id: UUID | None = None
    due_date: date | None = None
    resource_type: str | None = None
    resource_id: str | None = None
    resource_label: str | None = None


class TaskDecision(BaseModel):
    decision: str  # Approved | Rejected
    decision_comment: str | None = None


class TaskRead(BaseModel):
    id: UUID
    ref_id: str
    title: str
    description: str | None = None
    task_type: str
    status: str
    priority: str
    assignee_id: UUID | None = None
    assignee: UserRead | None = None
    created_by: UserRead | None = None
    due_date: date | None = None
    overdue: bool = False
    completed_at: datetime | None = None
    resource_type: str | None = None
    resource_id: str | None = None
    resource_label: str | None = None
    decision: str | None = None
    decision_comment: str | None = None
    decided_by: UserRead | None = None
    decided_at: datetime | None = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
