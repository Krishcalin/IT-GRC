"""Assessments — control self-assessments, maturity assessments, and vendor questionnaires.

An Assessment is a campaign of AssessmentItems. For a Control Self-Assessment /
Maturity Assessment each item is tied to a control and carries a CMMI-style
maturity (0–5) and/or a compliance result. For a Vendor Questionnaire each item is
a free-text question/answer linked (via the assessment) to a supplier. Scores are
derived from the items so progress is visible at a glance.
"""

from __future__ import annotations

import uuid
from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base

GOOD_RESULTS = {"Compliant", "Yes"}
RATED_RESULTS = {"Compliant", "Partial", "Non-Compliant", "Yes", "No"}


def aggregate_score(maturities: list[int | None], results: list[str | None]) -> float:
    """Single 0–100 score: maturity-weighted if any maturity is set, else from results."""
    mats = [m for m in maturities if m is not None]
    if mats:
        return round(sum(mats) / len(mats) / 5 * 100, 1)
    rated = [r for r in results if r in RATED_RESULTS]
    if rated:
        score = sum(1 for r in rated if r in GOOD_RESULTS) + sum(0.5 for r in rated if r == "Partial")
        return round(score / len(rated) * 100, 1)
    return 0.0


class Assessment(Base):
    __tablename__ = "assessments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ref_id: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)  # ASMT-001
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    assessment_type: Mapped[str] = mapped_column(String(40), default="Control Self-Assessment")  # Control Self-Assessment | Maturity Assessment | Vendor Questionnaire
    framework: Mapped[str | None] = mapped_column(String(48))  # scoping for control assessments
    supplier_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("suppliers.id", ondelete="SET NULL"))
    owner_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    status: Mapped[str] = mapped_column(String(24), default="Draft")  # Draft | In Progress | Submitted | Reviewed | Closed
    due_date: Mapped[date | None] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    owner: Mapped["User | None"] = relationship("User", foreign_keys=[owner_id], lazy="selectin")
    supplier: Mapped["Supplier | None"] = relationship("Supplier", foreign_keys=[supplier_id], lazy="selectin")
    items: Mapped[list["AssessmentItem"]] = relationship(
        "AssessmentItem", back_populates="assessment", lazy="selectin",
        cascade="all, delete-orphan", order_by="AssessmentItem.ref_id",
    )

    @property
    def item_count(self) -> int:
        return len(self.items)

    @property
    def answered_count(self) -> int:
        return sum(1 for i in self.items if i.maturity is not None or i.result)

    @property
    def avg_maturity(self) -> float | None:
        mats = [i.maturity for i in self.items if i.maturity is not None]
        return round(sum(mats) / len(mats), 1) if mats else None

    @property
    def score(self) -> float:
        return aggregate_score([i.maturity for i in self.items], [i.result for i in self.items])


class AssessmentItem(Base):
    __tablename__ = "assessment_items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ref_id: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)  # ASI-001
    assessment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False, index=True)
    control_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("controls.id", ondelete="SET NULL"))
    question: Mapped[str | None] = mapped_column(Text)  # prompt / questionnaire question
    response: Mapped[str | None] = mapped_column(Text)  # free-text answer / evidence
    maturity: Mapped[int | None] = mapped_column(Integer)  # CMMI 0–5
    result: Mapped[str | None] = mapped_column(String(20))  # Compliant | Partial | Non-Compliant | N/A | Yes | No
    comment: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    assessment: Mapped["Assessment"] = relationship("Assessment", back_populates="items")
    control: Mapped["Control | None"] = relationship("Control", foreign_keys=[control_id], lazy="selectin")
