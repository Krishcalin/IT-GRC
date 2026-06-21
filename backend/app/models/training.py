"""ISO 27001:2022 awareness & training models (Clauses 7.2 / 7.3, Annex A 6.3).

A TrainingCampaign represents an awareness campaign, course, or programme; its
TrainingRecords are the per-participant completion records that serve as evidence
of competence and awareness (7.2 d). Completion stats are derived from the records.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Date, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class TrainingCampaign(Base):
    __tablename__ = "training_campaigns"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ref_id: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)  # TRN-001
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    training_type: Mapped[str] = mapped_column(String(48), default="Awareness Campaign")  # Awareness Campaign | Onboarding | Role-based Training | Phishing Simulation | Policy Acknowledgment | Other
    topic: Mapped[str | None] = mapped_column(String(128))
    clause_ref: Mapped[str] = mapped_column(String(16), default="7.3")
    status: Mapped[str] = mapped_column(String(32), default="Planned")  # Planned | In Progress | Completed | Cancelled
    audience: Mapped[str | None] = mapped_column(String(256))  # target audience
    materials_link: Mapped[str | None] = mapped_column(String(512))
    owner_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    start_date: Mapped[datetime | None] = mapped_column(Date)
    end_date: Mapped[datetime | None] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    owner: Mapped["User | None"] = relationship("User", foreign_keys=[owner_id], lazy="selectin")
    records: Mapped[list["TrainingRecord"]] = relationship(
        "TrainingRecord", back_populates="campaign", lazy="selectin",
        cascade="all, delete-orphan", order_by="TrainingRecord.ref_id",
    )

    @property
    def total_participants(self) -> int:
        return len(self.records)

    @property
    def completed_participants(self) -> int:
        return sum(1 for r in self.records if r.status == "Completed")

    @property
    def completion_rate(self) -> float:
        total = len(self.records)
        return round(self.completed_participants / total * 100, 1) if total else 0.0


class TrainingRecord(Base):
    __tablename__ = "training_records"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ref_id: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)  # TRR-001
    campaign_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("training_campaigns.id", ondelete="CASCADE"), nullable=False)
    participant: Mapped[str] = mapped_column(String(128), nullable=False)  # name (may be an app user)
    user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    status: Mapped[str] = mapped_column(String(16), default="Assigned")  # Assigned | Completed | Overdue | Exempt
    score: Mapped[float | None] = mapped_column(Float)  # quiz / test score (%)
    completed_at: Mapped[datetime | None] = mapped_column(Date)
    evidence: Mapped[str | None] = mapped_column(String(512))  # proof-of-participation reference
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    campaign: Mapped["TrainingCampaign"] = relationship("TrainingCampaign", back_populates="records")
