# IT-GRC Portal — ISO 27001:2022

## Overview
Open-source IT Governance, Risk & Compliance portal for ISO 27001:2022 certification management. Full-stack web application with React frontend, FastAPI backend, and PostgreSQL database.

## Tech Stack
- **Frontend:** React 18 + TypeScript + Tailwind CSS + Vite + Recharts
- **Backend:** Python 3.12 + FastAPI + SQLAlchemy 2.0 (async) + Pydantic v2
- **Database:** PostgreSQL 16 with asyncpg driver
- **Auth:** JWT (python-jose) + bcrypt (passlib), SAML/OIDC ready
- **Deployment:** Docker Compose (3 containers: db, backend, frontend/nginx)

## Architecture

### Backend (`backend/app/`)
- `main.py` — FastAPI app with lifespan (creates tables + seeds on startup)
- `config.py` — Pydantic Settings from environment variables
- `database.py` — Async SQLAlchemy engine + session factory + Base
- `models/` — SQLAlchemy ORM models (all UUID PKs, timezone-aware timestamps)
- `schemas/` — Pydantic v2 request/response schemas (Create/Update/Read per model)
- `api/` — FastAPI route handlers (one file per module)
- `api/deps.py` — Shared dependencies (get_db, get_current_user, require_superuser)
- `seed/iso27001.py` — All 93 Annex A controls + 6 RBAC roles

### Frontend (`frontend/src/`)
- `App.tsx` — Root with AuthProvider + React Router
- `components/` — Layout, StatusBadge, DataTable (reusable)
- `pages/` — One page per module (Dashboard, Controls, Risks, SoA, Evidence, Audits, Policies, Assets, Login)
- `services/api.ts` — Axios client with JWT interceptor
- `hooks/useAuth.ts` — Auth context (login, logout, current user)
- `types/index.ts` — TypeScript interfaces matching backend schemas

### Database Models
| Model | Table | Key Fields |
|-------|-------|-----------|
| User | users | email, full_name, hashed_password, is_superuser, auth_provider |
| Role | roles | name, description, permissions (JSON) |
| Control | controls | clause (A.5.1), title, description, theme, status, owner_id |
| Risk | risks | ref_id (RISK-001), likelihood×impact scoring, treatment, status |
| SoAEntry | soa_entries | control_id (unique), applicable, implementation_status |
| Evidence | evidence | file_name, file_path, linked to control/risk/audit/policy |
| Audit | audits | ref_id (AUDIT-001), audit_type, status, findings[] |
| AuditFinding | audit_findings | ref_id (FIND-001), finding_type, severity, corrective_action |
| Policy | policies | ref_id (POL-001), version, status, content (markdown) |
| Asset | assets | ref_id (ASSET-001), asset_type, classification, criticality |
| ActivityLog | activity_log | user_id, action, resource_type, resource_id |

### RBAC Roles
- CISO: `["*"]` — full access
- GRC_Manager: controls/risks/audits/policies/soa/assets/evidence CRUD
- Risk_Owner: own risks + read controls
- Control_Owner: own controls + read risks
- Auditor: audits CRUD + read everything else
- Viewer: `["*:read"]` — read-only

### API Prefix
All API routes under `/api/v1/`. Swagger at `/docs`.

## ISO 27001:2022 Annex A
93 controls across 4 themes:
- A.5 Organizational (37): A.5.1 – A.5.37
- A.6 People (8): A.6.1 – A.6.8
- A.7 Physical (14): A.7.1 – A.7.14
- A.8 Technological (34): A.8.1 – A.8.34

Auto-seeded on first startup. Controls are read-only by default (update status/owner via PUT).

## Key Patterns
- All models use UUID primary keys
- Timestamps are timezone-aware UTC
- Risk levels computed from likelihood × impact (5×5 matrix)
- Ref IDs auto-generated: RISK-001, AUDIT-001, FIND-001, POL-001, ASSET-001
- File uploads stored in `backend/uploads/`, metadata in `evidence` table
- Activity logging on all create/update/delete operations

## Commands
```bash
# Start all services
docker compose up --build -d

# Backend dev server
cd backend && uvicorn app.main:app --reload --port 8000

# Frontend dev server
cd frontend && npm run dev

# Database migrations
cd backend && alembic revision --autogenerate -m "description"
cd backend && alembic upgrade head
```

## Environment Variables
See `.env.example`. Key variables:
- `DATABASE_URL` — PostgreSQL connection string
- `SECRET_KEY` — JWT signing key (change in production!)
- `FIRST_SUPERUSER_EMAIL/PASSWORD` — Initial admin credentials
- `SAML_METADATA_URL` / `OIDC_*` — Enterprise IdP configuration
