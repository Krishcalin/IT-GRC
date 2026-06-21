"""ISO 27001:2022 supplier / third-party register (Clauses 5.19–5.23).

Tracks supplier relationships and the information security expectations placed on
them: IS requirements agreed in agreements (5.20), ICT supply-chain and cloud
considerations (5.21/5.23), right-to-audit, certifications, criticality tiering,
and periodic monitoring/review (5.22).
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ref_id: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)  # SUP-001
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(32), default="Service")  # Product | Service | ICT Supply Chain | Cloud Service
    service_description: Mapped[str | None] = mapped_column(Text)  # what they provide
    criticality: Mapped[str] = mapped_column(String(16), default="Medium")  # Low | Medium | High | Critical
    data_classification: Mapped[str] = mapped_column(String(32), default="Internal")  # highest classification accessed
    status: Mapped[str] = mapped_column(String(32), default="Active")  # Active | Onboarding | Under Review | Offboarded
    is_requirements_agreed: Mapped[bool] = mapped_column(Boolean, default=False)  # IS requirements in agreement (5.20)
    right_to_audit: Mapped[bool] = mapped_column(Boolean, default=False)  # right-to-audit clause in contract
    processes_pii: Mapped[bool] = mapped_column(Boolean, default=False)  # handles personal data (DPA needed)
    certifications: Mapped[str | None] = mapped_column(String(256))  # e.g. "ISO 27001, SOC 2 Type II, TISAX"
    owner_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    contract_start: Mapped[datetime | None] = mapped_column(Date)
    contract_end: Mapped[datetime | None] = mapped_column(Date)
    last_review_date: Mapped[datetime | None] = mapped_column(Date)
    next_review_date: Mapped[datetime | None] = mapped_column(Date)
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    owner: Mapped["User | None"] = relationship("User", foreign_keys=[owner_id], lazy="selectin")
