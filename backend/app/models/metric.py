"""ISO 27001:2022 monitoring metrics (Clause 9.1) — KPI / KRI / KCI.

Key Performance / Risk / Control Indicators that monitor, measure, analyse, and
evaluate information security performance and ISMS effectiveness. Each metric
compares a target against the current (actual) value and yields a RAG status.
"""

from __future__ import annotations

import uuid
from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


def compute_rag(target: float | None, current: float | None, direction: str | None) -> str:
    """Derive a RAG status from target vs. current, respecting the metric direction."""
    if target is None or current is None:
        return "No Data"
    try:
        t, c = float(target), float(current)
    except (TypeError, ValueError):
        return "No Data"
    if direction == "lower_is_better":
        if c <= t:
            return "On Target"
        if t == 0:
            return "Off Target"
        return "Near Target" if c <= t * 1.1 else "Off Target"
    # default: higher_is_better
    if c >= t:
        return "On Target"
    if t == 0:
        return "On Target" if c >= 0 else "Off Target"
    return "Near Target" if c >= t * 0.9 else "Off Target"


class Metric(Base):
    __tablename__ = "metrics"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ref_id: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)  # MET-001
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    metric_type: Mapped[str] = mapped_column(String(8), default="KPI")  # KPI | KRI | KCI
    clause_ref: Mapped[str] = mapped_column(String(16), default="9.1")
    objective_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("objectives.id", ondelete="SET NULL"))
    target_value: Mapped[float | None] = mapped_column(Float)
    current_value: Mapped[float | None] = mapped_column(Float)
    unit: Mapped[str | None] = mapped_column(String(32))
    direction: Mapped[str] = mapped_column(String(20), default="higher_is_better")  # higher_is_better | lower_is_better
    frequency: Mapped[str | None] = mapped_column(String(32))  # Monthly | Quarterly | Annual | Continuous
    owner_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    last_measured: Mapped[datetime | None] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    owner: Mapped["User | None"] = relationship("User", foreign_keys=[owner_id], lazy="selectin")
    objective: Mapped["Objective | None"] = relationship("Objective", back_populates="metrics", lazy="selectin")
    measurements: Mapped[list["MetricMeasurement"]] = relationship(
        "MetricMeasurement", back_populates="metric", lazy="selectin",
        cascade="all, delete-orphan", order_by="MetricMeasurement.captured_at",
    )

    @property
    def rag(self) -> str:
        return compute_rag(self.target_value, self.current_value, self.direction)


class MetricMeasurement(Base):
    """A point-in-time measurement of a metric — the trend history behind KPIs/KRIs."""

    __tablename__ = "metric_measurements"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    metric_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("metrics.id", ondelete="CASCADE"), nullable=False, index=True)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    note: Mapped[str | None] = mapped_column(Text)
    captured_at: Mapped[date] = mapped_column(Date, default=lambda: datetime.now(timezone.utc).date(), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    metric: Mapped["Metric"] = relationship("Metric", back_populates="measurements")
