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
    # IS objectives (Clause 6.2) and metrics (Clause 9.1)
    total_objectives: int = 0
    achieved_objectives: int = 0
    objectives_by_status: dict = {}
    total_metrics: int = 0
    on_target_metrics: int = 0
    metrics_by_rag: dict = {}
    metrics_by_type: dict = {}
    # Suppliers / third parties (Clauses 5.19–5.23)
    total_suppliers: int = 0
    critical_suppliers: int = 0
    suppliers_by_criticality: dict = {}
    suppliers_by_category: dict = {}
    # Incidents (Clauses 5.24–5.28)
    total_incidents: int = 0
    open_incidents: int = 0
    incidents_by_severity: dict = {}
    incidents_by_status: dict = {}
    # Awareness & training (Clauses 7.2/7.3)
    total_campaigns: int = 0
    active_campaigns: int = 0
    training_completion_rate: float = 0.0
    campaigns_by_status: dict = {}
    # Reviews due (across registers)
    reviews_overdue: int = 0
    reviews_upcoming: int = 0
    # Workflow tasks
    total_tasks: int = 0
    open_tasks: int = 0
    overdue_tasks: int = 0
    pending_approvals: int = 0
    tasks_by_status: dict = {}
    tasks_by_priority: dict = {}
    # Assessments
    total_assessments: int = 0
    open_assessments: int = 0
    assessments_by_type: dict = {}
