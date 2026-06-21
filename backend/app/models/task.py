"""Workflow tasks & approvals.

A Task is a unit of accountable work — an assignment, a review, a remediation
action, or an approval/sign-off — that can be attached to any record in the
portal (control, risk, finding, incident, document, assessment, …) via a
lightweight polymorphic link (resource_type + resource_id). This is the
cross-cutting "workflow" layer that professional GRC tools (Archer, MetricStream)
are built around: every record can route work to an owner with a due date and an
audit-tracked sign-off.
"""

from __future__ import annotations

import uuid
from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base

# Statuses that mean the task is still outstanding (used for overdue / inbox logic).
TASK_OPEN_STATUSES = {"Open", "In Progress", "Blocked"}


def task_is_overdue(due_date: date | None, status: str, today: date | None = None) -> bool:
    """True when an open task's due date has passed. Pure + testable."""
    if not due_date or status not in TASK_OPEN_STATUSES:
        return False
    today = today or datetime.now(timezone.utc).date()
    return due_date < today


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ref_id: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)  # TASK-001
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    task_type: Mapped[str] = mapped_column(String(24), default="Action")  # Action | Approval | Review | Remediation
    status: Mapped[str] = mapped_column(String(24), default="Open", index=True)  # Open | In Progress | Blocked | Done | Cancelled
    priority: Mapped[str] = mapped_column(String(16), default="Medium")  # Low | Medium | High | Critical

    assignee_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), index=True)
    created_by_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    due_date: Mapped[date | None] = mapped_column(Date)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # Polymorphic link to the record this task relates to (optional — standalone tasks allowed).
    resource_type: Mapped[str | None] = mapped_column(String(32), index=True)  # control | risk | finding | incident | document | supplier | policy | assessment | objective | other
    resource_id: Mapped[str | None] = mapped_column(String(64))  # UUID or ref of the linked record
    resource_label: Mapped[str | None] = mapped_column(String(256))  # human label captured at creation

    # Approval / sign-off outcome (task_type == "Approval").
    decision: Mapped[str | None] = mapped_column(String(16))  # Approved | Rejected
    decision_comment: Mapped[str | None] = mapped_column(Text)
    decided_by_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    decided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    assignee: Mapped["User | None"] = relationship("User", foreign_keys=[assignee_id], lazy="selectin")
    created_by: Mapped["User | None"] = relationship("User", foreign_keys=[created_by_id], lazy="selectin")
    decided_by: Mapped["User | None"] = relationship("User", foreign_keys=[decided_by_id], lazy="selectin")

    @property
    def overdue(self) -> bool:
        return task_is_overdue(self.due_date, self.status)
