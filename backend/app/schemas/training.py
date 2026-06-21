"""Awareness & training (Clauses 7.2 / 7.3) schemas."""

from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from .user import UserRead


class TrainingRecordCreate(BaseModel):
    participant: str
    user_id: UUID | None = None
    status: str = "Assigned"
    score: float | None = None
    completed_at: date | None = None
    evidence: str | None = None


class TrainingRecordUpdate(BaseModel):
    participant: str | None = None
    user_id: UUID | None = None
    status: str | None = None
    score: float | None = None
    completed_at: date | None = None
    evidence: str | None = None


class TrainingRecordRead(BaseModel):
    id: UUID
    ref_id: str
    campaign_id: UUID
    participant: str
    user_id: UUID | None = None
    status: str
    score: float | None = None
    completed_at: date | None = None
    evidence: str | None = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class TrainingCampaignCreate(BaseModel):
    title: str
    description: str | None = None
    training_type: str = "Awareness Campaign"
    topic: str | None = None
    clause_ref: str = "7.3"
    status: str = "Planned"
    audience: str | None = None
    materials_link: str | None = None
    owner_id: UUID | None = None
    start_date: date | None = None
    end_date: date | None = None


class TrainingCampaignUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    training_type: str | None = None
    topic: str | None = None
    status: str | None = None
    audience: str | None = None
    materials_link: str | None = None
    owner_id: UUID | None = None
    start_date: date | None = None
    end_date: date | None = None


class TrainingCampaignRead(BaseModel):
    id: UUID
    ref_id: str
    title: str
    description: str | None = None
    training_type: str
    topic: str | None = None
    clause_ref: str
    status: str
    audience: str | None = None
    materials_link: str | None = None
    owner_id: UUID | None = None
    owner: UserRead | None = None
    start_date: date | None = None
    end_date: date | None = None
    total_participants: int
    completed_participants: int
    completion_rate: float
    records: list[TrainingRecordRead] = []
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
