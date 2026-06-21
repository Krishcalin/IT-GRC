"""FastAPI application entry point."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import settings
from .database import engine, Base, async_session

logger = logging.getLogger(__name__)


async def _run_seeds() -> None:
    """Seed the database with ISO 27001 controls, default roles, and first superuser."""
    from .seed.iso27001 import (
        seed_controls, seed_clauses, seed_documents, seed_interested_parties,
        seed_objectives, seed_metrics, seed_suppliers, seed_incidents,
        seed_training, seed_roles,
    )
    from .models.user import User
    from passlib.context import CryptContext
    from sqlalchemy import select, func

    pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async with async_session() as session:
        n_roles = await seed_roles(session)
        if n_roles:
            logger.info("Seeded %d RBAC roles", n_roles)

        n_controls = await seed_controls(session)
        if n_controls:
            logger.info("Seeded %d ISO 27001:2022 Annex A controls", n_controls)

        n_clauses = await seed_clauses(session)
        if n_clauses:
            logger.info("Seeded %d ISO 27001:2022 management-system clauses (4-10)", n_clauses)

        n_docs = await seed_documents(session)
        if n_docs:
            logger.info("Seeded %d mandatory documented-information records", n_docs)

        n_parties = await seed_interested_parties(session)
        if n_parties:
            logger.info("Seeded %d sample interested parties", n_parties)

        n_objectives = await seed_objectives(session)
        if n_objectives:
            logger.info("Seeded %d sample information security objectives", n_objectives)

        n_metrics = await seed_metrics(session)
        if n_metrics:
            logger.info("Seeded %d sample KPI/KRI/KCI metrics", n_metrics)

        n_suppliers = await seed_suppliers(session)
        if n_suppliers:
            logger.info("Seeded %d sample suppliers", n_suppliers)

        n_incidents = await seed_incidents(session)
        if n_incidents:
            logger.info("Seeded %d sample incidents", n_incidents)

        n_training = await seed_training(session)
        if n_training:
            logger.info("Seeded %d sample training campaigns", n_training)

        # Create first superuser if no users exist
        count = (await session.execute(select(func.count()).select_from(User))).scalar()
        if count == 0:
            user = User(
                email=settings.FIRST_SUPERUSER_EMAIL,
                full_name="System Administrator",
                hashed_password=pwd_ctx.hash(settings.FIRST_SUPERUSER_PASSWORD),
                is_superuser=True,
                is_active=True,
                auth_provider="local",
            )
            session.add(user)
            logger.info("Created first superuser: %s", settings.FIRST_SUPERUSER_EMAIL)

        await session.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created")

    await _run_seeds()
    logger.info("Seed data loaded")

    yield

    # Shutdown
    await engine.dispose()


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Open-source IT-GRC portal for ISO 27001:2022 compliance management",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register API routers ──────────────────────────────────
from .api.auth import router as auth_router        # noqa: E402
from .api.controls import router as controls_router  # noqa: E402
from .api.clauses import router as clauses_router     # noqa: E402
from .api.documents import router as documents_router  # noqa: E402
from .api.interested_parties import router as parties_router  # noqa: E402
from .api.objectives import router as objectives_router  # noqa: E402
from .api.metrics import router as metrics_router      # noqa: E402
from .api.suppliers import router as suppliers_router  # noqa: E402
from .api.incidents import router as incidents_router  # noqa: E402
from .api.training import router as training_router    # noqa: E402
from .api.reports import router as reports_router      # noqa: E402
from .api.risks import router as risks_router        # noqa: E402
from .api.soa import router as soa_router            # noqa: E402
from .api.evidence import router as evidence_router  # noqa: E402
from .api.audits import router as audits_router      # noqa: E402
from .api.policies import router as policies_router  # noqa: E402
from .api.assets import router as assets_router      # noqa: E402
from .api.dashboard import router as dashboard_router  # noqa: E402

app.include_router(auth_router, prefix=f"{settings.API_V1_PREFIX}/auth", tags=["Auth"])
app.include_router(controls_router, prefix=f"{settings.API_V1_PREFIX}/controls", tags=["Controls"])
app.include_router(clauses_router, prefix=f"{settings.API_V1_PREFIX}/clauses", tags=["ISMS Clauses"])
app.include_router(documents_router, prefix=f"{settings.API_V1_PREFIX}/documents", tags=["Documented Information"])
app.include_router(parties_router, prefix=f"{settings.API_V1_PREFIX}/interested-parties", tags=["Interested Parties"])
app.include_router(objectives_router, prefix=f"{settings.API_V1_PREFIX}/objectives", tags=["IS Objectives"])
app.include_router(metrics_router, prefix=f"{settings.API_V1_PREFIX}/metrics", tags=["Metrics (KPI/KRI/KCI)"])
app.include_router(suppliers_router, prefix=f"{settings.API_V1_PREFIX}/suppliers", tags=["Suppliers"])
app.include_router(incidents_router, prefix=f"{settings.API_V1_PREFIX}/incidents", tags=["Incidents"])
app.include_router(training_router, prefix=f"{settings.API_V1_PREFIX}/training", tags=["Awareness & Training"])
app.include_router(reports_router, prefix=f"{settings.API_V1_PREFIX}/reports", tags=["Reports"])
app.include_router(risks_router, prefix=f"{settings.API_V1_PREFIX}/risks", tags=["Risks"])
app.include_router(soa_router, prefix=f"{settings.API_V1_PREFIX}/soa", tags=["Statement of Applicability"])
app.include_router(evidence_router, prefix=f"{settings.API_V1_PREFIX}/evidence", tags=["Evidence"])
app.include_router(audits_router, prefix=f"{settings.API_V1_PREFIX}/audits", tags=["Audits"])
app.include_router(policies_router, prefix=f"{settings.API_V1_PREFIX}/policies", tags=["Policies"])
app.include_router(assets_router, prefix=f"{settings.API_V1_PREFIX}/assets", tags=["Assets"])
app.include_router(dashboard_router, prefix=f"{settings.API_V1_PREFIX}/dashboard", tags=["Dashboard"])


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}
