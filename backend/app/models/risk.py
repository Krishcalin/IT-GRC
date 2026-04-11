"""Risk Register models."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


def _risk_level(likelihood: int, impact: int) -> str:
    score = likelihood * impact
    if score >= 20:
        return "Critical"
    if score >= 12:
        return "High"
    if score >= 6:
        return "Medium"
    return "Low"


class Risk(Base):
    __tablename__ = "risks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ref_id: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)  # RISK-001
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(64), nullable=False)  # Strategic | Operational | Financial | Compliance | Technical | Reputational
    likelihood: Mapped[int] = mapped_column(Integer, default=1)  # 1-5
    impact: Mapped[int] = mapped_column(Integer, default=1)  # 1-5
    inherent_risk_level: Mapped[str] = mapped_column(String(16), default="Low")
    treatment: Mapped[str] = mapped_column(String(32), default="Mitigate")  # Mitigate | Accept | Transfer | Avoid
    treatment_plan: Mapped[str | None] = mapped_column(Text)
    residual_likelihood: Mapped[int | None] = mapped_column(Integer)
    residual_impact: Mapped[int | None] = mapped_column(Integer)
    residual_risk_level: Mapped[str | None] = mapped_column(String(16))
    owner_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    status: Mapped[str] = mapped_column(String(32), default="Open")  # Open | In Treatment | Closed | Accepted
    review_date: Mapped[datetime | None] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    owner: Mapped["User | None"] = relationship("User", foreign_keys=[owner_id], lazy="selectin")
    controls: Mapped[list["Control"]] = relationship(secondary="risk_controls", lazy="selectin")


class RiskControl(Base):
    __tablename__ = "risk_controls"

    risk_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("risks.id", ondelete="CASCADE"), primary_key=True)
    control_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("controls.id", ondelete="CASCADE"), primary_key=True)
