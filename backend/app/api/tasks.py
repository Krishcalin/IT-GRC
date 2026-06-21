"""Workflow task & approval routes.

A unified task/assignment layer that any module can attach work to. Supports a
"My Tasks" inbox (filter by assignee), overdue filtering, and an approval
sign-off endpoint that records the decision, decider, and timestamp.
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models.task import Task, task_is_overdue, TASK_OPEN_STATUSES
from ..models.user import User
from ..models.activity_log import ActivityLog
from ..schemas.task import TaskCreate, TaskUpdate, TaskRead, TaskDecision
from .deps import get_current_user

router = APIRouter()


@router.get("/", response_model=list[TaskRead])
async def list_tasks(
    status: str | None = None,
    task_type: str | None = None,
    priority: str | None = None,
    assignee_id: UUID | None = None,
    resource_type: str | None = None,
    resource_id: str | None = None,
    open_only: bool = False,
    overdue: bool = False,
    search: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(200, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    q = select(Task)
    if status:
        q = q.where(Task.status == status)
    if task_type:
        q = q.where(Task.task_type == task_type)
    if priority:
        q = q.where(Task.priority == priority)
    if assignee_id:
        q = q.where(Task.assignee_id == assignee_id)
    if resource_type:
        q = q.where(Task.resource_type == resource_type)
    if resource_id:
        q = q.where(Task.resource_id == resource_id)
    if open_only:
        q = q.where(Task.status.in_(TASK_OPEN_STATUSES))
    q = q.order_by(Task.due_date.is_(None), Task.due_date, Task.ref_id).offset(skip).limit(limit)
    rows = (await db.execute(q)).scalars().all()
    if overdue:
        rows = [t for t in rows if task_is_overdue(t.due_date, t.status)]
    if search:
        s = search.lower()
        rows = [t for t in rows if s in t.ref_id.lower() or s in t.title.lower()]
    return rows


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(task_id: UUID, db: AsyncSession = Depends(get_db)):
    task = (await db.execute(select(Task).where(Task.id == task_id))).scalar_one_or_none()
    if not task:
        raise HTTPException(404, "Task not found")
    return task


@router.post("/", response_model=TaskRead, status_code=201)
async def create_task(
    body: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    count = (await db.execute(select(func.count()).select_from(Task))).scalar() or 0
    task = Task(**body.model_dump(), ref_id=f"TASK-{count + 1:03d}", created_by_id=current_user.id)
    db.add(task)
    await db.flush()
    await db.refresh(task)
    db.add(ActivityLog(user_id=current_user.id, action="CREATE", resource_type="task", resource_id=str(task.id)))
    return task


@router.put("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: UUID,
    body: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = (await db.execute(select(Task).where(Task.id == task_id))).scalar_one_or_none()
    if not task:
        raise HTTPException(404, "Task not found")
    data = body.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(task, k, v)
    # Keep completed_at in sync with terminal status transitions.
    if "status" in data:
        if task.status == "Done" and task.completed_at is None:
            task.completed_at = datetime.now(timezone.utc)
        elif task.status in TASK_OPEN_STATUSES:
            task.completed_at = None
    await db.flush()
    await db.refresh(task)
    db.add(ActivityLog(user_id=current_user.id, action="UPDATE", resource_type="task", resource_id=str(task.id)))
    return task


@router.post("/{task_id}/decision", response_model=TaskRead)
async def decide_task(
    task_id: UUID,
    body: TaskDecision,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Record an approval/sign-off decision and close the task."""
    if body.decision not in ("Approved", "Rejected"):
        raise HTTPException(422, "decision must be 'Approved' or 'Rejected'")
    task = (await db.execute(select(Task).where(Task.id == task_id))).scalar_one_or_none()
    if not task:
        raise HTTPException(404, "Task not found")
    if task.task_type != "Approval":
        raise HTTPException(400, "Only approval tasks can be decided")
    task.decision = body.decision
    task.decision_comment = body.decision_comment
    task.decided_by_id = current_user.id
    task.decided_at = datetime.now(timezone.utc)
    task.status = "Done"
    task.completed_at = task.decided_at
    await db.flush()
    await db.refresh(task)
    db.add(ActivityLog(
        user_id=current_user.id, action=f"DECISION:{body.decision}",
        resource_type="task", resource_id=str(task.id),
    ))
    return task


@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = (await db.execute(select(Task).where(Task.id == task_id))).scalar_one_or_none()
    if not task:
        raise HTTPException(404, "Task not found")
    db.add(ActivityLog(user_id=current_user.id, action="DELETE", resource_type="task", resource_id=str(task.id)))
    await db.delete(task)
