"""ISO 27001:2022 information security incident register (Clauses 5.24–5.28).

Captures the incident lifecycle: planning/preparation (5.24), assessment and
decision on events (5.25), response (5.26), learning/root-cause (5.27), and
evidence collection (5.28).
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ref_id: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)  # INC-001
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)  # what happened
    category: Mapped[str] = mapped_column(String(48), default="Other")  # Malware | Phishing | Unauthorized Access | Data Breach | DoS | Misconfiguration | Lost/Stolen Device | Insider | Other
    severity: Mapped[str] = mapped_column(String(16), default="Medium")  # Low | Medium | High | Critical
    status: Mapped[str] = mapped_column(String(32), default="New")  # New | Triaged | In Progress | Resolved | Closed
    reporter: Mapped[str | None] = mapped_column(String(128))  # who reported it (may be external)
    reported_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    owner_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))  # incident handler
    risk_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("risks.id", ondelete="SET NULL"))  # related risk
    affected_assets: Mapped[str | None] = mapped_column(Text)  # affected information / IT systems
    data_breach: Mapped[bool] = mapped_column(Boolean, default=False)  # involves personal data / reportable breach
    containment_actions: Mapped[str | None] = mapped_column(Text)  # response / immediate measures (5.26)
    root_cause: Mapped[str | None] = mapped_column(Text)  # (5.27)
    lessons_learned: Mapped[str | None] = mapped_column(Text)  # (5.27)
    evidence_notes: Mapped[str | None] = mapped_column(Text)  # collection / preservation of evidence (5.28)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    owner: Mapped["User | None"] = relationship("User", foreign_keys=[owner_id], lazy="selectin")
