"""ISO 27001:2022 documented information (Clause 7.5) register.

Tracks the controlled documents and records that make up the ISMS — both the
documented information mandated by Clauses 4–10 and any further documents the
organization determines necessary. Supports the control requirements of 7.5.2
(identification, version, approval) and 7.5.3 (status, review, retention).
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class DocumentedInformation(Base):
    __tablename__ = "documented_information"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ref_id: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)  # DOC-001
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    doc_type: Mapped[str] = mapped_column(String(32), nullable=False)  # Policy | Process | Procedure | Plan | Register | Record | Statement | Guideline
    clause_ref: Mapped[str | None] = mapped_column(String(32), index=True)  # mandating clause, e.g. "6.1.3" / "A.5.1"
    mandatory: Mapped[bool] = mapped_column(Boolean, default=False)  # ISO-mandated documented information
    version: Mapped[str] = mapped_column(String(16), default="0.1")
    status: Mapped[str] = mapped_column(String(32), default="Draft")  # Draft | Under Review | Approved | Retired
    classification: Mapped[str] = mapped_column(String(32), default="Internal")  # Public | Internal | Confidential | Restricted
    location: Mapped[str | None] = mapped_column(String(512))  # link / path / repository reference
    owner_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    approver_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    review_date: Mapped[datetime | None] = mapped_column(Date)
    next_review_date: Mapped[datetime | None] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    owner: Mapped["User | None"] = relationship("User", foreign_keys=[owner_id], lazy="selectin")
    approver: Mapped["User | None"] = relationship("User", foreign_keys=[approver_id], lazy="selectin")
