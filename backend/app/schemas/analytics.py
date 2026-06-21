"""Analytics schemas — risk heat map, posture trend, personal work summary."""

from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class HeatCell(BaseModel):
    likelihood: int
    impact: int
    score: int
    level: str
    count: int


class RiskHeatmap(BaseModel):
    basis: str  # inherent | residual
    cells: list[HeatCell]
    total: int


class PostureSnapshotRead(BaseModel):
    snapshot_date: date
    compliance_score: float
    isms_conformity_score: float
    document_readiness_score: float
    training_completion_rate: float
    implemented_controls: int
    total_controls: int
    open_risks: int
    critical_risks: int
    open_findings: int
    open_tasks: int
    overdue_tasks: int
    model_config = ConfigDict(from_attributes=True)


class MyWork(BaseModel):
    open_tasks: int = 0
    overdue_tasks: int = 0
    pending_approvals: int = 0
    owned_controls: int = 0
    owned_risks: int = 0
    assigned_findings: int = 0
