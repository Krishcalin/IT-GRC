"""Posture snapshots — the time series behind compliance-score trend charts.

One row per day captures the headline ISMS posture (compliance, conformity,
document readiness, training completion) plus key counts, so the portal can show
how posture is trending rather than only a point-in-time figure. Snapshots are
captured automatically (once per day) when the dashboard stats are requested.
"""

from __future__ import annotations

import uuid
from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, Float, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class PostureSnapshot(Base):
    __tablename__ = "posture_snapshots"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    snapshot_date: Mapped[date] = mapped_column(Date, unique=True, nullable=False, index=True)
    compliance_score: Mapped[float] = mapped_column(Float, default=0.0)
    isms_conformity_score: Mapped[float] = mapped_column(Float, default=0.0)
    document_readiness_score: Mapped[float] = mapped_column(Float, default=0.0)
    training_completion_rate: Mapped[float] = mapped_column(Float, default=0.0)
    implemented_controls: Mapped[int] = mapped_column(Integer, default=0)
    total_controls: Mapped[int] = mapped_column(Integer, default=0)
    open_risks: Mapped[int] = mapped_column(Integer, default=0)
    critical_risks: Mapped[int] = mapped_column(Integer, default=0)
    open_findings: Mapped[int] = mapped_column(Integer, default=0)
    open_tasks: Mapped[int] = mapped_column(Integer, default=0)
    overdue_tasks: Mapped[int] = mapped_column(Integer, default=0)
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
