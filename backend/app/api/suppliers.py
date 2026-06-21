"""Supplier / third-party (Clauses 5.19–5.23) routes."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models.supplier import Supplier
from ..models.user import User
from ..models.activity_log import ActivityLog
from ..schemas.supplier import SupplierCreate, SupplierUpdate, SupplierRead
from .deps import get_current_user

router = APIRouter()


@router.get("/", response_model=list[SupplierRead])
async def list_suppliers(
    category: str | None = None,
    criticality: str | None = None,
    status: str | None = None,
    search: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(200, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    q = select(Supplier)
    if category:
        q = q.where(Supplier.category == category)
    if criticality:
        q = q.where(Supplier.criticality == criticality)
    if status:
        q = q.where(Supplier.status == status)
    if search:
        q = q.where(or_(Supplier.ref_id.ilike(f"%{search}%"), Supplier.name.ilike(f"%{search}%")))
    q = q.order_by(Supplier.ref_id).offset(skip).limit(limit)
    return (await db.execute(q)).scalars().all()


@router.post("/", response_model=SupplierRead, status_code=201)
async def create_supplier(
    body: SupplierCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    count = (await db.execute(select(func.count()).select_from(Supplier))).scalar() or 0
    ref_id = f"SUP-{count + 1:03d}"
    supplier = Supplier(**body.model_dump(), ref_id=ref_id)
    db.add(supplier)
    await db.flush()
    await db.refresh(supplier)
    db.add(ActivityLog(user_id=current_user.id, action="CREATE", resource_type="supplier", resource_id=str(supplier.id)))
    return supplier


@router.get("/{supplier_id}", response_model=SupplierRead)
async def get_supplier(supplier_id: UUID, db: AsyncSession = Depends(get_db)):
    supplier = (await db.execute(select(Supplier).where(Supplier.id == supplier_id))).scalar_one_or_none()
    if not supplier:
        raise HTTPException(404, "Supplier not found")
    return supplier


@router.put("/{supplier_id}", response_model=SupplierRead)
async def update_supplier(
    supplier_id: UUID,
    body: SupplierUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    supplier = (await db.execute(select(Supplier).where(Supplier.id == supplier_id))).scalar_one_or_none()
    if not supplier:
        raise HTTPException(404, "Supplier not found")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(supplier, k, v)
    await db.flush()
    await db.refresh(supplier)
    db.add(ActivityLog(user_id=current_user.id, action="UPDATE", resource_type="supplier", resource_id=str(supplier.id)))
    return supplier


@router.delete("/{supplier_id}", status_code=204)
async def delete_supplier(
    supplier_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    supplier = (await db.execute(select(Supplier).where(Supplier.id == supplier_id))).scalar_one_or_none()
    if not supplier:
        raise HTTPException(404, "Supplier not found")
    db.add(ActivityLog(user_id=current_user.id, action="DELETE", resource_type="supplier", resource_id=str(supplier.id)))
    await db.delete(supplier)
