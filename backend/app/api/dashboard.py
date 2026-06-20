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
from ..models.risk import Risk
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
