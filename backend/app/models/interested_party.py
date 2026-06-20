"""ISO 27001:2022 interested parties (Clause 4.2) register.

Records the interested parties relevant to the ISMS, their relevant requirements
(legal, regulatory, contractual, expectations), and — per Clause 4.2(c) — which
of those requirements are addressed through the ISMS.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class InterestedParty(Base):
    __tablename__ = "interested_parties"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ref_id: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)  # PARTY-001
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    party_type: Mapped[str] = mapped_column(String(16), default="External")  # Internal | External
    category: Mapped[str] = mapped_column(String(48), nullable=False)  # Customer | Regulator | Employee | Supplier | Partner | Owner | Other
    requirements: Mapped[str | None] = mapped_column(Text)  # their relevant requirements / expectations
    addressed_in_isms: Mapped[bool] = mapped_column(Boolean, default=False)  # Clause 4.2(c)
    notes: Mapped[str | None] = mapped_column(Text)
    owner_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    owner: Mapped["User | None"] = relationship("User", foreign_keys=[owner_id], lazy="selectin")
