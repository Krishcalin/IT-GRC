"""Statement of Applicability model."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class SoAEntry(Base):
    __tablename__ = "soa_entries"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    control_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("controls.id", ondelete="CASCADE"), unique=True, nullable=False)
    applicable: Mapped[bool] = mapped_column(Boolean, default=True)
    justification: Mapped[str | None] = mapped_column(Text)  # required when not applicable
    implementation_status: Mapped[str] = mapped_column(String(32), default="Not Implemented")  # Not Implemented | Partially | Fully | N/A
    implementation_evidence: Mapped[str | None] = mapped_column(Text)
    responsible_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    control: Mapped["Control"] = relationship("Control", back_populates="soa_entry", lazy="selectin")
    responsible: Mapped["User | None"] = relationship("User", foreign_keys=[responsible_id], lazy="selectin")
