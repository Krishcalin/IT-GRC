"""Dashboard statistics schema."""

from __future__ import annotations

from pydantic import BaseModel


class DashboardStats(BaseModel):
    total_controls: int = 0
    implemented_controls: int = 0
    total_risks: int = 0
    open_risks: int = 0
    critical_risks: int = 0
    total_audits: int = 0
    open_findings: int = 0
    total_policies: int = 0
    total_assets: int = 0
    compliance_score: float = 0.0
    risk_posture: dict = {}
    controls_by_status: dict = {}
    controls_by_theme: dict = {}
