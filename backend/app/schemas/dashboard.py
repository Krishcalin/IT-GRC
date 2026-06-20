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
    # ISMS management-system clauses (4–10)
    total_clauses: int = 0
    conformant_clauses: int = 0
    isms_conformity_score: float = 0.0
    clauses_by_status: dict = {}
    clauses_by_section: dict = {}
    # Documented information (Clause 7.5) and interested parties (Clause 4.2)
    total_documents: int = 0
    mandatory_documents: int = 0
    approved_mandatory_documents: int = 0
    document_readiness_score: float = 0.0
    documents_by_status: dict = {}
    total_interested_parties: int = 0
