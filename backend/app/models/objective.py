"""ISO 27001:2022 information security objectives (Clause 6.2) model.

Objectives are the measurable goals of the ISMS, consistent with the policy and
informed by risk assessment. Each objective can be measured by one or more
Metrics (KPI/KRI/KCI — see :mod:`.metric`, Clause 9.1).
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Date, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class Objective(Base):
    __tablename__ = "objectives"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ref_id: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)  # OBJ-001
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    clause_ref: Mapped[str] = mapped_column(String(16), default="6.2")
    measure: Mapped[str | None] = mapped_column(Text)  # how achievement is measured
    target_value: Mapped[str | None] = mapped_column(String(128))  # textual target, e.g. "<= 5%"
    current_value: Mapped[str | None] = mapped_column(String(128))
    unit: Mapped[str | None] = mapped_column(String(32))
    status: Mapped[str] = mapped_column(String(32), default="Not Started")  # Not Started | On Track | At Risk | Achieved | Missed
    owner_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    due_date: Mapped[datetime | None] = mapped_column(Date)
    review_date: Mapped[datetime | None] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    owner: Mapped["User | None"] = relationship("User", foreign_keys=[owner_id], lazy="selectin")
    metrics: Mapped[list["Metric"]] = relationship(
        "Metric", back_populates="objective", lazy="selectin", order_by="Metric.ref_id",
    )
