"""Reminders / notifications — items whose review or due date is overdue or upcoming.

Scans the review/due dates across the ISMS registers (controls, clauses, documents,
suppliers, policies, risks, objectives) and returns a single categorized list, so
nothing silently lapses. `gather_reminders` is reused by the dashboard for counts.
"""

from __future__ import annotations

from datetime import date, timedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models.control import Control
from ..models.clause_requirement import ClauseRequirement
from ..models.documented_information import DocumentedInformation
from ..models.supplier import Supplier
from ..models.policy import Policy
from ..models.risk import Risk
from ..models.objective import Objective
from ..models.user import User
from .deps import get_current_user

router = APIRouter()


def _item(category: str, ref: str, title: str, due: date, link: str, today: date) -> dict:
    return {
        "category": category,
        "ref_id": ref,
        "title": title,
        "due_date": due.isoformat(),
        "kind": "overdue" if due < today else "upcoming",
        "link": link,
    }


async def gather_reminders(db: AsyncSession, window_days: int = 30) -> dict:
    today = date.today()
    cutoff = today + timedelta(days=window_days)
    items: list[dict] = []

    for c in (await db.execute(select(Control).where(Control.review_date <= cutoff))).scalars():
        items.append(_item("Control", c.clause, c.title, c.review_date, f"/controls/{c.id}", today))
    for c in (await db.execute(select(ClauseRequirement).where(ClauseRequirement.review_date <= cutoff))).scalars():
        items.append(_item("ISMS Clause", c.clause, c.title, c.review_date, f"/clauses/{c.id}", today))
    for d in (await db.execute(select(DocumentedInformation).where(DocumentedInformation.next_review_date <= cutoff))).scalars():
        items.append(_item("Document", d.ref_id, d.title, d.next_review_date, f"/documents/{d.id}", today))
    for s in (await db.execute(select(Supplier).where(Supplier.next_review_date <= cutoff))).scalars():
        items.append(_item("Supplier", s.ref_id, s.name, s.next_review_date, f"/suppliers/{s.id}", today))
    for p in (await db.execute(select(Policy).where(Policy.next_review_date <= cutoff))).scalars():
        items.append(_item("Policy", p.ref_id, p.title, p.next_review_date, "/policies", today))
    for r in (await db.execute(select(Risk).where(Risk.review_date <= cutoff))).scalars():
        items.append(_item("Risk", r.ref_id, r.title, r.review_date, f"/risks/{r.id}", today))
    for o in (await db.execute(select(Objective).where(Objective.review_date <= cutoff))).scalars():
        items.append(_item("Objective", o.ref_id, o.title, o.review_date, f"/objectives/{o.id}", today))

    items.sort(key=lambda x: x["due_date"])
    overdue = sum(1 for i in items if i["kind"] == "overdue")
    return {
        "as_of": today.isoformat(),
        "window_days": window_days,
        "overdue_count": overdue,
        "upcoming_count": len(items) - overdue,
        "items": items,
    }


@router.get("/")
async def list_reminders(
    window_days: int = Query(30, ge=0, le=365),
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return await gather_reminders(db, window_days)
