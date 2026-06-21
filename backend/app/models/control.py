"""ISO 27001:2022 Annex A Control model."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Date, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class Control(Base):
    __tablename__ = "controls"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    clause: Mapped[str] = mapped_column(String(16), unique=True, nullable=False, index=True)  # e.g. "A.5.1", "ENR.8.40"
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    # Source control set: "ISO 27001:2022" (Annex A) or "ISO 27019:2024" (energy-utility sector controls)
    framework: Mapped[str] = mapped_column(String(48), nullable=False, default="ISO 27001:2022", server_default="ISO 27001:2022", index=True)
    theme: Mapped[str] = mapped_column(String(32), nullable=False)  # Organizational | People | Physical | Technological
    implementation_guidance: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(32), default="Not Started")  # Not Started | In Progress | Implemented | Not Applicable
    owner_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    review_date: Mapped[datetime | None] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    owner: Mapped["User | None"] = relationship("User", foreign_keys=[owner_id], lazy="selectin")
    soa_entry: Mapped["SoAEntry | None"] = relationship("SoAEntry", back_populates="control", uselist=False, lazy="selectin")
