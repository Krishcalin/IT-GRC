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
- `api/` — FastAPI route handlers, one file per module: `auth`, `controls`, `clauses`, `documents`, `interested_parties`, `objectives`, `metrics`, `risks`, `soa`, `evidence`, `audits`, `policies`, `assets`, `dashboard`
- `api/deps.py` — Shared dependencies (get_db, get_current_user, require_superuser)
- `seed/iso27001.py` — 93 Annex A controls + 30 ISMS clauses (4–10) + 17 mandatory documents + sample interested parties + sample objectives & KPI/KRI/KCI metrics + 6 RBAC roles

### Frontend (`frontend/src/`)
- `App.tsx` — Root with AuthProvider + React Router
- `components/` — `Layout` (sidebar shell) and `StatusBadge` (status/theme/conformity/RAG pill)
- `pages/` — One page per module (Dashboard, Controls, ISMS Clauses, Interested Parties, IS Objectives, Metrics, Risks, SoA, Evidence, Documents, Audits, Policies, Assets, Login) plus detail pages (`ControlDetailPage`, `ClauseDetailPage`, `DocumentDetailPage`, `ObjectiveDetailPage`, `MetricDetailPage`, `AuditDetailPage`)
- `services/api.ts` — Axios client with JWT interceptor
- `hooks/useAuth.ts` — Auth context (login, logout, current user)
- `types/index.ts` — TypeScript interfaces matching backend schemas

### Database Models
| Model | Table | Key Fields |
|-------|-------|-----------|
| User | users | email, full_name, hashed_password, is_superuser, auth_provider |
| Role | roles | name, description, permissions (JSON) |
| Control | controls | clause (A.5.1), title, description, theme, status, owner_id |
| ClauseRequirement | clause_requirements | clause (6.1.2), title, section, clause_number, requirement, documented_info, conformity_status, owner_id |
| DocumentedInformation | documented_information | ref_id (DOC-001), title, doc_type, clause_ref, mandatory, version, status, classification, owner/approver, review dates |
| InterestedParty | interested_parties | ref_id (PARTY-001), name, party_type, category, requirements, addressed_in_isms |
| Objective | objectives | ref_id (OBJ-001), title, clause_ref (6.2), measure, target/current_value, status, owner_id, metrics[] |
| Metric | metrics | ref_id (MET-001), name, metric_type (KPI/KRI/KCI), objective_id, target/current_value, direction, frequency, rag (derived) |
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
All API routes under `/api/v1/`. Swagger at `/docs`, ReDoc at `/redoc`, health at `/health`.

| Resource | Routes |
|----------|--------|
| `/auth` | `login`, `me` |
| `/controls` | list / get / create / update / delete (Annex A) |
| `/clauses` | list / get / create / update / delete (ISMS Clauses 4–10) |
| `/documents` | list / get / create / update / delete (Documented Information 7.5) |
| `/interested-parties` | list / get / create / update / delete (Interested Parties 4.2) |
| `/objectives` | list / get / create / update / delete (IS Objectives 6.2; embeds metrics) |
| `/metrics` | list / get / create / update / delete (KPI/KRI/KCI 9.1; derived RAG) |
| `/risks` | list / get / create / update / delete |
| `/soa` | list / create / update |
| `/evidence` | list / upload / download |
| `/audits` | audits + nested `findings` |
| `/policies` | list / get / create / update / acknowledge |
| `/assets` | list / get / create / update / delete |
| `/dashboard` | `stats`, `activity` |

`/dashboard/stats` returns control posture (by status/theme), risk posture, ISMS
clause conformity (total, conformant, conformity score, by status/section),
documented-information readiness (mandatory vs approved, by status), interested-party
count, IS objective status, metric RAG/type breakdown, the compliance score, and module counts.

## ISO 27001:2022 Annex A
93 controls across 4 themes:
- A.5 Organizational (37): A.5.1 – A.5.37
- A.6 People (8): A.6.1 – A.6.8
- A.7 Physical (14): A.7.1 – A.7.14
- A.8 Technological (34): A.8.1 – A.8.34

Auto-seeded on first startup. Controls are read-only by default (update status/owner via PUT).

## ISO 27001:2022 Clauses 4–10 (mandatory ISMS requirements)
30 management-system requirements seeded into `clause_requirements`, tracked for
conformity separately from Annex A controls. Per Clause 1 (Scope), none may be
excluded when claiming conformity, so there is no "Not Applicable" status.
- 4 Context of the organization (4): 4.1–4.4
- 5 Leadership (3): 5.1–5.3
- 6 Planning (5): 6.1.1, 6.1.2, 6.1.3, 6.2, 6.3
- 7 Support (7): 7.1–7.4, 7.5.1–7.5.3
- 8 Operation (3): 8.1–8.3
- 9 Performance evaluation (6): 9.1, 9.2.1, 9.2.2, 9.3.1–9.3.3
- 10 Improvement (2): 10.1, 10.2

Each clause carries the (paraphrased) requirement text, the mandatory documented
information it demands (where applicable), a `conformity_status` (Not Assessed /
In Progress / Partially Conformant / Conformant / Nonconformant), owner, and
review date. API at `/api/v1/clauses`; UI at `/clauses`. Requirement text is
paraphrased — ISO/IEC 27001:2022 is the authoritative source.

## Documented Information (Clause 7.5)
A controlled-document register (`documented_information`) covering 7.5.2 (identity,
version, approval) and 7.5.3 (status, review, retention). Seeded on first startup
with the **17 mandatory documents/records** required across Clauses 4–10 (Scope,
IS Policy, risk assessment/treatment processes, SoA, risk treatment plan, IS
objectives, competence evidence, operational/risk-assessment/risk-treatment
results, monitoring results, audit programme & results, management-review results,
nonconformity & corrective-action records, plus the interested-parties and legal
registers), each linked to its clause and flagged `mandatory`. Statuses: Draft /
Under Review / Approved / Retired. Ref IDs `DOC-001…`. API `/api/v1/documents`;
UI `/documents` (+ detail page). Dashboard surfaces a **document readiness** score
(approved mandatory ÷ mandatory).

## Interested Parties (Clause 4.2)
A stakeholder register (`interested_parties`): name, `party_type` (Internal/External),
`category` (Customer/Regulator/Employee/Supplier/Partner/Owner/Other), their
`requirements`, and `addressed_in_isms` (Clause 4.2c). Seeded with a representative
starter set; ref IDs `PARTY-001…`. API `/api/v1/interested-parties`; UI
`/interested-parties`.

## IS Objectives (Clause 6.2) & Metrics / KxI (Clause 9.1)
Two linked registers covering the ISACA guide's "IS Objectives" and
"Performance/Risk/Compliance Monitoring" building blocks.

- **Objectives** (`objectives`, ref `OBJ-001`): measurable ISMS goals with a
  textual target/current, owner, due/review dates, and `status` (Not Started /
  On Track / At Risk / Achieved / Missed). `ObjectiveRead` embeds its metrics.
- **Metrics** (`metrics`, ref `MET-001`): KPI / KRI / KCI indicators with numeric
  `target_value` vs `current_value`, a `direction` (higher/lower is better), and
  `frequency`. A **RAG status** (`On Target` / `Near Target` / `Off Target` /
  `No Data`) is derived by `compute_rag()` in `models/metric.py` (used by both the
  `MetricRead.rag` property and the dashboard). Each metric optionally links to an
  objective (`objective_id`).
- Seeded with a small sample set (3 objectives, 5 metrics) demonstrating the
  target-vs-actual model. Dashboard adds objectives-by-status and metric-RAG charts.
- API `/api/v1/objectives` and `/api/v1/metrics`; UI `/objectives` and `/metrics`
  (each with a detail page).

> Identified next-tranche gaps from the ISACA Implementation Guide (not yet built):
> Supplier register (5.19–5.23), Incident management (5.24–5.28),
> Awareness/training (7.2/7.3).

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
