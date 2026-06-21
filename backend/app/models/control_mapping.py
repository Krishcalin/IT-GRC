"""Control-to-control crosswalk — the "unified control framework" layer.

Maps a control in one framework to a related control in another (e.g. ISO 27001
A.8.16 ↔ NIST CSF DE.CM ↔ SOC 2 CC7). Lets an organization satisfy multiple
frameworks from one control set ("test once, comply many") and drives coverage /
gap analysis across frameworks.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class ControlMapping(Base):
    __tablename__ = "control_mappings"
    __table_args__ = (UniqueConstraint("source_control_id", "target_control_id", name="uq_control_mapping"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_control_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("controls.id", ondelete="CASCADE"), nullable=False, index=True)
    target_control_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("controls.id", ondelete="CASCADE"), nullable=False, index=True)
    relationship_type: Mapped[str] = mapped_column(String(16), default="related")  # equivalent | related | broader | narrower
    note: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    source_control: Mapped["Control"] = relationship("Control", foreign_keys=[source_control_id], lazy="selectin")
    target_control: Mapped["Control"] = relationship("Control", foreign_keys=[target_control_id], lazy="selectin")
