"""Dashboard statistics routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models.control import Control
from ..models.clause_requirement import ClauseRequirement
from ..models.documented_information import DocumentedInformation
from ..models.interested_party import InterestedParty
from ..models.objective import Objective
from ..models.metric import Metric, compute_rag
from ..models.supplier import Supplier
from ..models.incident import Incident
from ..models.training import TrainingCampaign, TrainingRecord
from ..models.risk import Risk
from .reminders import gather_reminders
from ..models.task import Task, task_is_overdue, TASK_OPEN_STATUSES
from ..models.audit import Audit, AuditFinding
from ..models.policy import Policy
from ..models.asset import Asset
from ..models.soa import SoAEntry
from ..models.activity_log import ActivityLog
from ..schemas.dashboard import DashboardStats
from .deps import get_current_user

router = APIRouter()


@router.get("/stats", response_model=DashboardStats)
async def get_stats(db: AsyncSession = Depends(get_db)):
    # Controls
    total_controls = (await db.execute(select(func.count()).select_from(Control))).scalar() or 0
    implemented = (await db.execute(
        select(func.count()).select_from(Control).where(Control.status == "Implemented")
    )).scalar() or 0

    # Controls by status
    status_rows = (await db.execute(
        select(Control.status, func.count()).group_by(Control.status)
    )).all()
    controls_by_status = {row[0]: row[1] for row in status_rows}

    # Controls by theme
    theme_rows = (await db.execute(
        select(Control.theme, func.count()).group_by(Control.theme)
    )).all()
    controls_by_theme = {row[0]: row[1] for row in theme_rows}

    # ISMS management-system clauses (4–10)
    total_clauses = (await db.execute(select(func.count()).select_from(ClauseRequirement))).scalar() or 0
    conformant_clauses = (await db.execute(
        select(func.count()).select_from(ClauseRequirement).where(ClauseRequirement.conformity_status == "Conformant")
    )).scalar() or 0
    clause_status_rows = (await db.execute(
        select(ClauseRequirement.conformity_status, func.count()).group_by(ClauseRequirement.conformity_status)
    )).all()
    clauses_by_status = {row[0]: row[1] for row in clause_status_rows}
    clause_section_rows = (await db.execute(
        select(ClauseRequirement.section, func.count()).group_by(ClauseRequirement.section)
    )).all()
    clauses_by_section = {row[0]: row[1] for row in clause_section_rows}
    isms_conformity_score = round((conformant_clauses / total_clauses * 100) if total_clauses > 0 else 0, 1)

    # Documented information (Clause 7.5)
    total_documents = (await db.execute(select(func.count()).select_from(DocumentedInformation))).scalar() or 0
    mandatory_documents = (await db.execute(
        select(func.count()).select_from(DocumentedInformation).where(DocumentedInformation.mandatory == True)
    )).scalar() or 0
    approved_mandatory_documents = (await db.execute(
        select(func.count()).select_from(DocumentedInformation).where(
            DocumentedInformation.mandatory == True, DocumentedInformation.status == "Approved"
        )
    )).scalar() or 0
    doc_status_rows = (await db.execute(
        select(DocumentedInformation.status, func.count()).group_by(DocumentedInformation.status)
    )).all()
    documents_by_status = {row[0]: row[1] for row in doc_status_rows}
    document_readiness_score = round(
        (approved_mandatory_documents / mandatory_documents * 100) if mandatory_documents > 0 else 0, 1
    )

    # Interested parties (Clause 4.2)
    total_interested_parties = (await db.execute(select(func.count()).select_from(InterestedParty))).scalar() or 0

    # IS objectives (Clause 6.2)
    total_objectives = (await db.execute(select(func.count()).select_from(Objective))).scalar() or 0
    achieved_objectives = (await db.execute(
        select(func.count()).select_from(Objective).where(Objective.status == "Achieved")
    )).scalar() or 0
    obj_status_rows = (await db.execute(
        select(Objective.status, func.count()).group_by(Objective.status)
    )).all()
    objectives_by_status = {row[0]: row[1] for row in obj_status_rows}

    # Metrics (Clause 9.1) — RAG derived per metric
    metric_rows = (await db.execute(select(Metric))).scalars().all()
    total_metrics = len(metric_rows)
    metrics_by_rag: dict = {}
    metrics_by_type: dict = {}
    for m in metric_rows:
        rag = compute_rag(m.target_value, m.current_value, m.direction)
        metrics_by_rag[rag] = metrics_by_rag.get(rag, 0) + 1
        metrics_by_type[m.metric_type] = metrics_by_type.get(m.metric_type, 0) + 1
    on_target_metrics = metrics_by_rag.get("On Target", 0)

    # Suppliers / third parties (Clauses 5.19–5.23)
    total_suppliers = (await db.execute(select(func.count()).select_from(Supplier))).scalar() or 0
    critical_suppliers = (await db.execute(
        select(func.count()).select_from(Supplier).where(Supplier.criticality.in_(["High", "Critical"]))
    )).scalar() or 0
    sup_crit_rows = (await db.execute(
        select(Supplier.criticality, func.count()).group_by(Supplier.criticality)
    )).all()
    suppliers_by_criticality = {row[0]: row[1] for row in sup_crit_rows}
    sup_cat_rows = (await db.execute(
        select(Supplier.category, func.count()).group_by(Supplier.category)
    )).all()
    suppliers_by_category = {row[0]: row[1] for row in sup_cat_rows}

    # Incidents (Clauses 5.24–5.28)
    total_incidents = (await db.execute(select(func.count()).select_from(Incident))).scalar() or 0
    open_incidents = (await db.execute(
        select(func.count()).select_from(Incident).where(Incident.status.notin_(["Resolved", "Closed"]))
    )).scalar() or 0
    inc_sev_rows = (await db.execute(
        select(Incident.severity, func.count()).group_by(Incident.severity)
    )).all()
    incidents_by_severity = {row[0]: row[1] for row in inc_sev_rows}
    inc_status_rows = (await db.execute(
        select(Incident.status, func.count()).group_by(Incident.status)
    )).all()
    incidents_by_status = {row[0]: row[1] for row in inc_status_rows}

    # Awareness & training (Clauses 7.2/7.3)
    total_campaigns = (await db.execute(select(func.count()).select_from(TrainingCampaign))).scalar() or 0
    active_campaigns = (await db.execute(
        select(func.count()).select_from(TrainingCampaign).where(TrainingCampaign.status == "In Progress")
    )).scalar() or 0
    camp_status_rows = (await db.execute(
        select(TrainingCampaign.status, func.count()).group_by(TrainingCampaign.status)
    )).all()
    campaigns_by_status = {row[0]: row[1] for row in camp_status_rows}
    total_records = (await db.execute(select(func.count()).select_from(TrainingRecord))).scalar() or 0
    completed_records = (await db.execute(
        select(func.count()).select_from(TrainingRecord).where(TrainingRecord.status == "Completed")
    )).scalar() or 0
    training_completion_rate = round((completed_records / total_records * 100) if total_records else 0, 1)

    # Reviews due across registers
    reminders = await gather_reminders(db)
    reviews_overdue = reminders["overdue_count"]
    reviews_upcoming = reminders["upcoming_count"]

    # Workflow tasks
    task_rows = (await db.execute(select(Task))).scalars().all()
    total_tasks = len(task_rows)
    open_tasks = sum(1 for t in task_rows if t.status in TASK_OPEN_STATUSES)
    overdue_tasks = sum(1 for t in task_rows if task_is_overdue(t.due_date, t.status))
    pending_approvals = sum(1 for t in task_rows if t.task_type == "Approval" and t.status in TASK_OPEN_STATUSES)
    tasks_by_status: dict = {}
    tasks_by_priority: dict = {}
    for t in task_rows:
        tasks_by_status[t.status] = tasks_by_status.get(t.status, 0) + 1
        tasks_by_priority[t.priority] = tasks_by_priority.get(t.priority, 0) + 1

    # Risks
    total_risks = (await db.execute(select(func.count()).select_from(Risk))).scalar() or 0
    open_risks = (await db.execute(
        select(func.count()).select_from(Risk).where(Risk.status.in_(["Open", "In Treatment"]))
    )).scalar() or 0
    critical_risks = (await db.execute(
        select(func.count()).select_from(Risk).where(Risk.inherent_risk_level == "Critical")
    )).scalar() or 0

    # Risk posture
    risk_rows = (await db.execute(
        select(Risk.inherent_risk_level, func.count()).group_by(Risk.inherent_risk_level)
    )).all()
    risk_posture = {row[0]: row[1] for row in risk_rows}

    # Audits & findings
    total_audits = (await db.execute(select(func.count()).select_from(Audit))).scalar() or 0
    open_findings = (await db.execute(
        select(func.count()).select_from(AuditFinding).where(AuditFinding.status.in_(["Open", "In Progress"]))
    )).scalar() or 0

    # Policies & assets
    total_policies = (await db.execute(select(func.count()).select_from(Policy))).scalar() or 0
    total_assets = (await db.execute(select(func.count()).select_from(Asset))).scalar() or 0

    # Compliance score: implemented / total applicable SoA entries
    total_applicable = (await db.execute(
        select(func.count()).select_from(SoAEntry).where(SoAEntry.applicable == True)
    )).scalar() or 0
    fully_implemented = (await db.execute(
        select(func.count()).select_from(SoAEntry).where(
            SoAEntry.applicable == True, SoAEntry.implementation_status == "Fully Implemented"
        )
    )).scalar() or 0
    compliance_score = round((fully_implemented / total_applicable * 100) if total_applicable > 0 else (implemented / total_controls * 100) if total_controls > 0 else 0, 1)

    # Record today's posture snapshot (idempotent per day) so the trend grows automatically.
    from .analytics import compute_headline, record_posture_snapshot
    try:
        await record_posture_snapshot(db, await compute_headline(db))
    except Exception:  # never let snapshotting break the dashboard
        pass

    return DashboardStats(
        total_controls=total_controls,
        implemented_controls=implemented,
        total_risks=total_risks,
        open_risks=open_risks,
        critical_risks=critical_risks,
        total_audits=total_audits,
        open_findings=open_findings,
        total_policies=total_policies,
        total_assets=total_assets,
        compliance_score=compliance_score,
        risk_posture=risk_posture,
        controls_by_status=controls_by_status,
        controls_by_theme=controls_by_theme,
        total_clauses=total_clauses,
        conformant_clauses=conformant_clauses,
        isms_conformity_score=isms_conformity_score,
        clauses_by_status=clauses_by_status,
        clauses_by_section=clauses_by_section,
        total_documents=total_documents,
        mandatory_documents=mandatory_documents,
        approved_mandatory_documents=approved_mandatory_documents,
        document_readiness_score=document_readiness_score,
        documents_by_status=documents_by_status,
        total_interested_parties=total_interested_parties,
        total_objectives=total_objectives,
        achieved_objectives=achieved_objectives,
        objectives_by_status=objectives_by_status,
        total_metrics=total_metrics,
        on_target_metrics=on_target_metrics,
        metrics_by_rag=metrics_by_rag,
        metrics_by_type=metrics_by_type,
        total_suppliers=total_suppliers,
        critical_suppliers=critical_suppliers,
        suppliers_by_criticality=suppliers_by_criticality,
        suppliers_by_category=suppliers_by_category,
        total_incidents=total_incidents,
        open_incidents=open_incidents,
        incidents_by_severity=incidents_by_severity,
        incidents_by_status=incidents_by_status,
        total_campaigns=total_campaigns,
        active_campaigns=active_campaigns,
        training_completion_rate=training_completion_rate,
        campaigns_by_status=campaigns_by_status,
        reviews_overdue=reviews_overdue,
        reviews_upcoming=reviews_upcoming,
        total_tasks=total_tasks,
        open_tasks=open_tasks,
        overdue_tasks=overdue_tasks,
        pending_approvals=pending_approvals,
        tasks_by_status=tasks_by_status,
        tasks_by_priority=tasks_by_priority,
    )


@router.get("/activity")
async def get_activity(
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    rows = (await db.execute(
        select(ActivityLog).order_by(ActivityLog.created_at.desc()).limit(limit)
    )).scalars().all()
    return [
        {
            "id": str(r.id),
            "user_id": str(r.user_id) if r.user_id else None,
            "action": r.action,
            "resource_type": r.resource_type,
            "resource_id": r.resource_id,
            "details": r.details,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in rows
    ]
