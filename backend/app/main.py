"""FastAPI application entry point."""

from __future__ import annotations

import asyncio
import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import settings
from .database import engine, async_session

logger = logging.getLogger(__name__)


async def _run_seeds() -> None:
    """Seed the database with ISO 27001 controls, default roles, and first superuser."""
    from .seed.iso27001 import (
        seed_controls, seed_iso27019_controls, seed_nist_csf_controls, seed_soc2_controls,
        seed_iec62443_controls, seed_control_mappings, seed_clauses, seed_documents,
        seed_interested_parties, seed_objectives, seed_metrics, seed_metric_history,
        seed_posture_snapshots, seed_suppliers, seed_incidents, seed_training,
        seed_assessments, seed_tasks, seed_roles,
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

        n_enr = await seed_iso27019_controls(session)
        if n_enr:
            logger.info("Seeded %d ISO 27019:2024 energy-sector controls", n_enr)

        n_csf = await seed_nist_csf_controls(session)
        if n_csf:
            logger.info("Seeded %d NIST CSF 2.0 categories", n_csf)

        n_soc2 = await seed_soc2_controls(session)
        if n_soc2:
            logger.info("Seeded %d SOC 2 criteria", n_soc2)

        n_iec = await seed_iec62443_controls(session)
        if n_iec:
            logger.info("Seeded %d IEC 62443-2-1:2024 OT security-program elements", n_iec)

        n_maps = await seed_control_mappings(session)
        if n_maps:
            logger.info("Seeded %d cross-framework control mappings", n_maps)

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

        n_history = await seed_metric_history(session)
        if n_history:
            logger.info("Seeded %d metric measurement points", n_history)

        n_snapshots = await seed_posture_snapshots(session)
        if n_snapshots:
            logger.info("Seeded %d posture snapshots", n_snapshots)

        n_suppliers = await seed_suppliers(session)
        if n_suppliers:
            logger.info("Seeded %d sample suppliers", n_suppliers)

        n_incidents = await seed_incidents(session)
        if n_incidents:
            logger.info("Seeded %d sample incidents", n_incidents)

        n_training = await seed_training(session)
        if n_training:
            logger.info("Seeded %d sample training campaigns", n_training)

        n_assessments = await seed_assessments(session)
        if n_assessments:
            logger.info("Seeded %d sample assessments", n_assessments)

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
            await session.flush()  # ensure a user exists before seeding sample tasks
            logger.info("Created first superuser: %s", settings.FIRST_SUPERUSER_EMAIL)

        n_tasks = await seed_tasks(session)
        if n_tasks:
            logger.info("Seeded %d sample workflow tasks", n_tasks)

        await session.commit()


_MIGRATION_LOCK_KEY = 8127342  # arbitrary constant id for the migration advisory lock


async def _run_migrations() -> None:
    """Bring the database schema up to head via Alembic.

    Runs ``alembic upgrade head`` as a subprocess (avoids nesting Alembic's own
    asyncio.run inside the running event loop). Replaces the previous
    create_all + ad-hoc ALTER approach so all schema changes are version-controlled.

    A Postgres transaction-level advisory lock serializes the upgrade across uvicorn
    workers (the lifespan runs in every worker): one worker performs the upgrade
    while the others block, then run an idempotent no-op upgrade. The lock is
    released automatically when the surrounding transaction ends.
    """
    from sqlalchemy import text

    backend_dir = Path(__file__).resolve().parents[1]  # .../backend (holds alembic.ini)
    async with engine.begin() as conn:
        await conn.execute(text("SELECT pg_advisory_xact_lock(:k)"), {"k": _MIGRATION_LOCK_KEY})
        proc = await asyncio.create_subprocess_exec(
            sys.executable, "-m", "alembic", "upgrade", "head",
            cwd=str(backend_dir),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )
        out, _ = await proc.communicate()
        if out:
            logger.info("alembic upgrade head:\n%s", out.decode(errors="replace").strip())
        if proc.returncode != 0:
            raise RuntimeError(f"alembic upgrade head failed (exit code {proc.returncode})")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await _run_migrations()
    logger.info("Database schema is at head (Alembic)")

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
from .api.reminders import router as reminders_router  # noqa: E402
from .api.tasks import router as tasks_router          # noqa: E402
from .api.analytics import router as analytics_router  # noqa: E402
from .api.assessments import router as assessments_router  # noqa: E402
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
app.include_router(reminders_router, prefix=f"{settings.API_V1_PREFIX}/reminders", tags=["Reminders"])
app.include_router(tasks_router, prefix=f"{settings.API_V1_PREFIX}/tasks", tags=["Tasks & Workflow"])
app.include_router(analytics_router, prefix=f"{settings.API_V1_PREFIX}/analytics", tags=["Analytics"])
app.include_router(assessments_router, prefix=f"{settings.API_V1_PREFIX}/assessments", tags=["Assessments"])
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
