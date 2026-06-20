"""ISO 27001:2022 mandatory management-system clause (Clauses 4–10) model.

These are the normative ISMS requirements an organization is audited against for
certification — distinct from the Annex A controls (see :mod:`.control`). Annex A
controls may be excluded with justification; the Clause 4–10 requirements are
mandatory and cannot be excluded when claiming conformity.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class ClauseRequirement(Base):
    __tablename__ = "clause_requirements"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    clause: Mapped[str] = mapped_column(String(16), unique=True, nullable=False, index=True)  # e.g. "6.1.2"
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    section: Mapped[str] = mapped_column(String(64), nullable=False)  # e.g. "Planning"
    clause_number: Mapped[int] = mapped_column(Integer, nullable=False, index=True)  # 4..10
    requirement: Mapped[str] = mapped_column(Text, nullable=False)  # paraphrased "shall" requirement
    documented_info: Mapped[str | None] = mapped_column(Text)  # mandatory documented information, if any
    conformity_status: Mapped[str] = mapped_column(String(32), default="Not Assessed")  # Not Assessed | In Progress | Partially Conformant | Conformant | Nonconformant
    implementation_notes: Mapped[str | None] = mapped_column(Text)
    owner_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    review_date: Mapped[datetime | None] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    owner: Mapped["User | None"] = relationship("User", foreign_keys=[owner_id], lazy="selectin")
