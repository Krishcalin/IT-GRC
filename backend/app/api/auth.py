"""Authentication routes."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import settings
from ..database import get_db
from ..models.user import User
from ..models.activity_log import ActivityLog
from ..schemas.auth import Token, LoginRequest
from ..schemas.user import UserCreate, UserRead
from .deps import get_current_user, require_superuser

router = APIRouter()
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _create_token(user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub": user_id, "exp": expire}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


@router.post("/login", response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = (await db.execute(select(User).where(User.email == form.username))).scalar_one_or_none()
    if not user or not user.hashed_password or not pwd_ctx.verify(form.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is disabled")

    db.add(ActivityLog(user_id=user.id, action="LOGIN", resource_type="user", resource_id=str(user.id)))
    return Token(access_token=_create_token(str(user.id)))


@router.post("/login/json", response_model=Token)
async def login_json(body: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = (await db.execute(select(User).where(User.email == body.email))).scalar_one_or_none()
    if not user or not user.hashed_password or not pwd_ctx.verify(body.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is disabled")

    db.add(ActivityLog(user_id=user.id, action="LOGIN", resource_type="user", resource_id=str(user.id)))
    return Token(access_token=_create_token(str(user.id)))


@router.post("/register", response_model=UserRead)
async def register(
    body: UserCreate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_superuser),
):
    existing = (await db.execute(select(User).where(User.email == body.email))).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=body.email,
        full_name=body.full_name,
        hashed_password=pwd_ctx.hash(body.password),
        department=body.department,
        is_superuser=body.is_superuser,
        auth_provider="local",
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)

    db.add(ActivityLog(user_id=admin.id, action="CREATE", resource_type="user", resource_id=str(user.id)))
    return user


@router.get("/me", response_model=UserRead)
async def me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/users", response_model=list[UserRead])
async def list_users(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """Active users — used to populate assignee/owner pickers across the portal."""
    rows = (await db.execute(
        select(User).where(User.is_active == True).order_by(User.full_name)
    )).scalars().all()
    return rows
