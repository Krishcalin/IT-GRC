"""Reporting & export routes — CSV exports and a printable board-pack.

Dependency-free: CSV via the stdlib `csv` module, and a self-contained HTML
board pack the browser can print to PDF. All endpoints require authentication;
the frontend downloads them as blobs (carrying the JWT) like evidence downloads.
"""

from __future__ import annotations

import csv
import io
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Response
from fastapi.responses import HTMLResponse
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models.control import Control
from ..models.clause_requirement import ClauseRequirement
from ..models.documented_information import DocumentedInformation
from ..models.risk import Risk
from ..models.soa import SoAEntry
from ..models.incident import Incident
from ..models.supplier import Supplier
from ..models.training import TrainingRecord
from ..models.user import User
from .deps import get_current_user

router = APIRouter()


def _csv(filename: str, header: list[str], rows: list[list]) -> Response:
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(header)
    writer.writerows(rows)
    return Response(
        content=buf.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/soa.csv")
async def export_soa(db: AsyncSession = Depends(get_db), _: User = Depends(get_current_user)):
    entries = (await db.execute(select(SoAEntry))).scalars().all()
    rows = []
    for e in sorted(entries, key=lambda x: x.control.clause if x.control else ""):
        c = e.control
        rows.append([
            c.clause if c else "", c.title if c else "", c.theme if c else "",
            "Yes" if e.applicable else "No", e.implementation_status,
            e.justification or "", e.responsible.full_name if e.responsible else "", e.notes or "",
        ])
    return _csv("statement_of_applicability.csv",
                ["Clause", "Control", "Theme", "Applicable", "Implementation Status", "Justification", "Responsible", "Notes"],
                rows)


@router.get("/risks.csv")
async def export_risks(db: AsyncSession = Depends(get_db), _: User = Depends(get_current_user)):
    risks = (await db.execute(select(Risk).order_by(Risk.ref_id))).scalars().all()
    rows = [[
        r.ref_id, r.title, r.category, r.likelihood, r.impact, r.inherent_risk_level,
        r.treatment, r.residual_risk_level or "", r.status,
        r.owner.full_name if r.owner else "", r.review_date.isoformat() if r.review_date else "",
    ] for r in risks]
    return _csv("risk_register.csv",
                ["Ref", "Title", "Category", "Likelihood", "Impact", "Inherent Level", "Treatment", "Residual Level", "Status", "Owner", "Review Date"],
                rows)


@router.get("/controls.csv")
async def export_controls(db: AsyncSession = Depends(get_db), _: User = Depends(get_current_user)):
    controls = (await db.execute(select(Control).order_by(Control.framework, Control.clause))).scalars().all()
    rows = [[
        c.clause, c.title, c.theme, c.framework, c.status,
        c.owner.full_name if c.owner else "", c.review_date.isoformat() if c.review_date else "",
    ] for c in controls]
    return _csv("controls.csv",
                ["Clause", "Title", "Theme", "Framework", "Status", "Owner", "Review Date"], rows)


async def _count(db: AsyncSession, model, *where) -> int:
    q = select(func.count()).select_from(model)
    for w in where:
        q = q.where(w)
    return (await db.execute(q)).scalar() or 0


@router.get("/board-pack.html", response_class=HTMLResponse)
async def board_pack(db: AsyncSession = Depends(get_db), _: User = Depends(get_current_user)):
    total_controls = await _count(db, Control)
    implemented = await _count(db, Control, Control.status == "Implemented")
    total_clauses = await _count(db, ClauseRequirement)
    conformant = await _count(db, ClauseRequirement, ClauseRequirement.conformity_status == "Conformant")
    mandatory_docs = await _count(db, DocumentedInformation, DocumentedInformation.mandatory == True)
    approved_docs = await _count(db, DocumentedInformation, DocumentedInformation.mandatory == True, DocumentedInformation.status == "Approved")
    total_risks = await _count(db, Risk)
    open_risks = await _count(db, Risk, Risk.status.in_(["Open", "In Treatment"]))
    critical_risks = await _count(db, Risk, Risk.inherent_risk_level == "Critical")
    open_incidents = await _count(db, Incident, Incident.status.notin_(["Resolved", "Closed"]))
    total_suppliers = await _count(db, Supplier)
    high_suppliers = await _count(db, Supplier, Supplier.criticality.in_(["High", "Critical"]))

    total_applicable = await _count(db, SoAEntry, SoAEntry.applicable == True)
    fully = await _count(db, SoAEntry, SoAEntry.applicable == True, SoAEntry.implementation_status == "Fully Implemented")
    compliance = round((fully / total_applicable * 100) if total_applicable else (implemented / total_controls * 100) if total_controls else 0, 1)
    conformity = round((conformant / total_clauses * 100) if total_clauses else 0, 1)
    doc_readiness = round((approved_docs / mandatory_docs * 100) if mandatory_docs else 0, 1)

    total_records = await _count(db, TrainingRecord)
    completed_records = await _count(db, TrainingRecord, TrainingRecord.status == "Completed")
    training_completion = round((completed_records / total_records * 100) if total_records else 0, 1)

    # Top risks by score
    risks = (await db.execute(select(Risk))).scalars().all()
    top = sorted(risks, key=lambda r: r.likelihood * r.impact, reverse=True)[:5]
    top_rows = "".join(
        f"<tr><td>{r.ref_id}</td><td>{r.title}</td><td>{r.category}</td>"
        f"<td class='lvl {r.inherent_risk_level.lower()}'>{r.inherent_risk_level}</td><td>{r.status}</td></tr>"
        for r in top
    ) or "<tr><td colspan='5' class='muted'>No risks recorded</td></tr>"

    today = datetime.now(timezone.utc).date().isoformat()

    def card(label, value, suffix=""):
        return f"<div class='card'><div class='val'>{value}{suffix}</div><div class='lbl'>{label}</div></div>"

    cards = "".join([
        card("Compliance Score", compliance, "%"),
        card("ISMS Conformity", conformity, "%"),
        card("Document Readiness", doc_readiness, "%"),
        card("Training Completion", training_completion, "%"),
        card("Implemented Controls", f"{implemented}/{total_controls}"),
        card("Open Risks", open_risks),
        card("Critical Risks", critical_risks),
        card("Open Incidents", open_incidents),
        card("Suppliers (High/Critical)", f"{high_suppliers}/{total_suppliers}"),
    ])

    html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>ISMS Board Pack — {today}</title>
<style>
 * {{ box-sizing: border-box; }}
 body {{ font-family: -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; color: #1f2937; margin: 0; padding: 40px; }}
 h1 {{ font-size: 24px; margin: 0 0 4px; }}
 .sub {{ color: #6b7280; margin-bottom: 28px; }}
 .grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 32px; }}
 .card {{ border: 1px solid #e5e7eb; border-radius: 12px; padding: 18px; }}
 .val {{ font-size: 28px; font-weight: 700; color: #4f46e5; }}
 .lbl {{ color: #6b7280; font-size: 13px; margin-top: 4px; }}
 h2 {{ font-size: 16px; margin: 24px 0 12px; }}
 table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
 th, td {{ text-align: left; padding: 8px 10px; border-bottom: 1px solid #eee; }}
 th {{ background: #f9fafb; color: #374151; }}
 .muted {{ color: #9ca3af; text-align: center; }}
 .lvl {{ font-weight: 600; }} .critical {{ color: #dc2626; }} .high {{ color: #ea580c; }} .medium {{ color: #d97706; }} .low {{ color: #0d9488; }}
 .foot {{ margin-top: 40px; color: #9ca3af; font-size: 12px; }}
 @media print {{ body {{ padding: 0; }} .noprint {{ display: none; }} }}
</style></head><body>
 <button class="noprint" onclick="window.print()" style="float:right;padding:8px 16px;border:1px solid #4f46e5;background:#4f46e5;color:#fff;border-radius:8px;cursor:pointer">Print / Save PDF</button>
 <h1>ISMS Board Pack</h1>
 <div class="sub">ISO/IEC 27001:2022 — information security posture summary · generated {today}</div>
 <div class="grid">{cards}</div>
 <h2>Top Risks</h2>
 <table><thead><tr><th>Ref</th><th>Title</th><th>Category</th><th>Level</th><th>Status</th></tr></thead><tbody>{top_rows}</tbody></table>
 <div class="foot">Generated by the IT-GRC portal. Figures reflect current register data and are intended for management review.</div>
</body></html>"""
    return HTMLResponse(content=html)
