<p align="center">
  <img src="banner.svg" alt="IT-GRC Portal — Unified Governance, Risk & Compliance for IT & OT" width="100%">
</p>

# IT-GRC Portal — ISO 27001:2022

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)](https://react.dev)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)](https://postgresql.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![ISO 27001](https://img.shields.io/badge/ISO_27001-2022-blue)](https://www.iso.org/standard/27001)
[![Controls](https://img.shields.io/badge/Annex_A_Controls-93-orange)](#controls-library)
[![ISO 27019](https://img.shields.io/badge/ISO_27019_(Energy)-12-teal)](#isoiec-270192024-energy-sector-coverage)
[![IEC 62443](https://img.shields.io/badge/IEC_62443--2--1_(OT)-8_SPEs-darkgreen)](#additional-frameworks--crosswalk)
[![Frameworks](https://img.shields.io/badge/Frameworks-5_cross--mapped-blueviolet)](#additional-frameworks--crosswalk)
[![ISMS Clauses](https://img.shields.io/badge/ISMS_Clauses_4--10-30-9cf)](#isms-clause-conformity-clauses-410)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](#quick-start)
[![CI](https://github.com/Krishcalin/IT-GRC/actions/workflows/ci.yml/badge.svg)](https://github.com/Krishcalin/IT-GRC/actions/workflows/ci.yml)

An **open-source IT Governance, Risk & Compliance (GRC) portal** purpose-built for **ISO 27001:2022** certification management. Clone it, deploy internally with Docker Compose, integrate with your corporate IdP (SAML/OIDC), and start managing your ISMS.

---

## Features

### Workflow & Task Management
- Cross-cutting **task/assignment layer** any record can route work to — actions, reviews, remediation, and **approvals/sign-off**
- **"My Tasks" inbox** (filter by assignee) plus an all-tasks board with status, type, priority, and search filters
- **Due dates with overdue (SLA) flagging** and a dashboard panel for open / overdue / pending-approval counts
- **Approval tasks** capture an Approved/Rejected decision, the decider, a comment, and timestamp — an audit-tracked sign-off
- Tasks link to any module record (control, risk, finding, incident, document, supplier, policy, …) via a lightweight reference

### Analytics & Dashboards
- **Risk heat map** — a 5×5 likelihood × impact matrix (inherent or residual basis) with per-cell risk counts and level colouring
- **ISMS posture trend** — compliance, conformity, document-readiness, and training-completion scores tracked over time (snapshots captured automatically each day)
- **KPI/KRI/KCI trend history** — record point-in-time measurements per metric and chart the trend against its target
- **Role/owner-aware "My Work"** panel on the dashboard (my open/overdue tasks, approvals, owned controls/risks, assigned findings)
- Dashboard **Workflow & Tasks** panel (open / overdue / pending approvals + by-status/priority charts)

### Controls Library
- All **93 Annex A controls** from ISO 27001:2022 pre-loaded and categorized by theme
- 4 themes: Organizational (37), People (8), Physical (14), Technological (34)
- **12 ISO/IEC 27019:2024 energy-sector controls** (the "ENR" controls for SCADA/ICS in the energy utility industry) loaded as an additional, filterable framework
- Track implementation status, assign owners, set review dates
- Link controls to risks, evidence, and audit findings
- Filter the library by **framework** (ISO 27001:2022 / ISO 27019:2024 / NIST CSF 2.0 / SOC 2 / IEC 62443-2-1:2024), theme, and status

### Unified Control Framework (Multi-Framework & Crosswalk)
- Multiple control catalogs in one place: **ISO 27001:2022 (93)**, **ISO 27019:2024 (12)**, **NIST CSF 2.0 (22 categories)**, **SOC 2 (13 criteria)**, **IEC 62443-2-1:2024 (8 OT program elements)**
- **Control-to-control crosswalk** — map a control to equivalent/related controls in other frameworks ("test once, comply many"), editable from any control's detail page
- **Cross-framework coverage matrix** — see what % of each framework's controls map to each other framework, with a per-framework coverage summary
- Pre-seeded crosswalks: ISO 27001 ↔ NIST CSF, ISO 27001 ↔ SOC 2, and **ISO 27001/27019 ↔ IEC 62443** (the IT-ISMS ↔ OT-security-program bridge for energy/ICS)

### Assessments & Attestations
- **Control self-assessments** with **CMMI-style maturity scoring (0–5)** and a derived posture score
- **One-click "populate from framework"** — generate assessment items for every control in a chosen framework
- **Vendor security questionnaires** — Q&A items (Yes/No/Partial) with a derived compliance score, linkable to a supplier
- Per-assessment **score, average maturity, and progress** (answered/total), with status workflow (Draft → In Progress → Submitted → Reviewed → Closed)
- **Policy acknowledgment / attestation** — users attest to policies (existing Policies module: `POST /policies/{id}/acknowledge`)

### ISMS Clause Conformity (Clauses 4–10)
- All **30 mandatory management-system requirements** from ISO 27001:2022 Clauses 4–10 pre-loaded
- Organized by section: Context, Leadership, Planning, Support, Operation, Performance evaluation, Improvement
- Track conformity status (Not Assessed → In Progress → Partially Conformant → Conformant / Nonconformant), assign owners, set review dates
- Each clause flags the **mandatory documented information** it requires (scope, policy, SoA, objectives, audit/management-review records, etc.)
- Distinct from Annex A controls — per Clause 1 (Scope), these clauses cannot be excluded when claiming conformity

### Documented Information Register (Clause 7.5)
- The **17 mandatory documents and records** required across Clauses 4–10 pre-loaded as a checklist, each linked to its clause
- Controlled-document lifecycle: identity, version, classification, approval, and review dates (7.5.2/7.5.3)
- Status tracking (Draft → Under Review → Approved → Retired) and a dashboard **document-readiness** score
- Add your own organization-specific documents alongside the mandatory set

### Interested Parties Register (Clause 4.2)
- Catalog the parties relevant to the ISMS (customers, regulators, employees, suppliers, owners…)
- Record their relevant requirements/expectations (legal, regulatory, contractual)
- Flag whether each party's requirements are **addressed by the ISMS** (Clause 4.2c)

### IS Objectives & KPIs (Clauses 6.2 / 9.1)
- Define **measurable information security objectives** with targets, owners, and status (On Track → At Risk → Achieved / Missed)
- Track **KPIs / KRIs / KCIs** — Key Performance, Risk, and Control Indicators with a numeric target vs. current value
- Each metric auto-derives a **RAG status** (On Target / Near Target / Off Target) honouring whether higher or lower is better
- Link metrics to the objectives they measure; dashboard shows objectives-by-status and metric-RAG breakdowns

### Supplier / Third-Party Register (Clauses 5.19–5.23)
- Catalog suppliers by **ISO 27036-1 category** (Product / Service / ICT Supply Chain / Cloud Service) and **criticality**
- Record whether **IS requirements are agreed** in the contract (5.20), the **right-to-audit** clause, and whether the supplier **processes PII**
- Capture **certifications** (ISO 27001, SOC 2, TISAX…), contract dates, and periodic **review dates** (5.22)
- Dashboard shows suppliers by criticality and by category

### Incident Management (Clauses 5.24–5.28)
- Record security incidents with **category**, **severity**, and a lifecycle **status** (New → Triaged → In Progress → Resolved → Closed)
- Capture the response chain: **containment** (5.26), **root cause & lessons learned** (5.27), and **evidence notes** (5.28)
- Flag **personal-data / reportable breaches**, track reporter, affected assets, and auto-stamped resolution time
- Dashboard shows incidents by severity and status plus an **open-incident** count

### Awareness & Training (Clauses 7.2 / 7.3)
- Plan **awareness campaigns / courses** (type, topic, audience, materials, dates) with a lifecycle status
- Track **per-participant completion records** — the evidence of competence (7.2 d) — with status, score, and proof
- Each campaign shows an **auto-computed completion rate**; manage participants inline (add, mark complete, change status)
- Dashboard shows overall **training completion %** and campaigns by status

### Risk Register
- Create and manage information security risks with full lifecycle tracking
- **5x5 risk matrix** — likelihood × impact scoring (Low / Medium / High / Critical)
- Risk treatment options: Mitigate, Accept, Transfer, Avoid
- Track inherent vs. residual risk levels
- Link risks to controls and assets

### Statement of Applicability (SoA)
- One entry per Annex A control — applicable/not applicable with justification
- Track implementation status: Not Implemented → Partially → Fully Implemented
- Export full SoA for auditor review
- Assign responsible persons per control

### Evidence Management
- Upload and organize audit evidence (documents, screenshots, configs)
- Link evidence to controls, risks, audits, or policies
- File metadata tracking: type, size, uploader, upload date
- Download evidence files directly from the portal

### Audit Management
- Plan and track internal, external, and surveillance audits
- Record audit findings: Major NC, Minor NC, Observation, OFI
- Assign corrective actions with due dates and owners
- Track finding lifecycle: Open → In Progress → Resolved → Verified

### Policy Management
- Create and version information security policies (Markdown content)
- Policy lifecycle: Draft → Under Review → Approved → Retired
- Track policy acknowledgments by users
- Automatic review date reminders

### Asset Inventory
- Catalog information assets: Hardware, Software, Data, Service, People, Facility
- Asset classification: Public, Internal, Confidential, Restricted
- Link assets to risks for impact analysis
- Track asset criticality and ownership

### Dashboard
- Real-time compliance posture score
- Controls by status and theme (charts)
- ISMS clause conformity score + clauses by conformity and section (charts)
- Open risks and critical findings at a glance
- Recent activity feed

### Authentication & RBAC
- **Local auth** with bcrypt-hashed passwords and JWT tokens
- **SAML/OIDC** integration ready for enterprise IdPs
- Role-based access control:
  - **CISO** — full access
  - **GRC Manager** — manage all modules
  - **Risk Owner** — manage assigned risks
  - **Control Owner** — manage assigned controls
  - **Auditor** — manage audits, read-only elsewhere
  - **Viewer** — read-only access

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 18 + TypeScript + Tailwind CSS + Recharts |
| **Backend** | Python 3.12 + FastAPI + SQLAlchemy 2.0 (async) |
| **Database** | PostgreSQL 16 |
| **Auth** | JWT + bcrypt, SAML/OIDC ready |
| **Deployment** | Docker Compose |

---

## Quick Start

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/IT-GRC.git
cd IT-GRC
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env — at minimum change SECRET_KEY and FIRST_SUPERUSER_PASSWORD
```

### 3. Build and launch

```bash
docker compose up --build -d
```

### 4. Access the portal

| Service | URL |
|---------|-----|
| **Frontend** | http://localhost:3000 |
| **Backend API** | http://localhost:8000 |
| **API Docs (Swagger)** | http://localhost:8000/docs |
| **Health Check** | http://localhost:8000/health |

### 5. Login

Use the credentials from your `.env` file:
- **Email:** `admin@company.com` (default)
- **Password:** `Admin@123` (default — change immediately)

On first startup, the system automatically:
- Applies database migrations (`alembic upgrade head`)
- Seeds 93 ISO 27001:2022 Annex A controls
- Seeds 12 ISO/IEC 27019:2024 energy-sector (ENR) controls
- Seeds 22 NIST CSF 2.0 categories + 13 SOC 2 criteria + 8 IEC 62443-2-1:2024 OT program elements and a starter cross-framework crosswalk (incl. ISO ↔ IEC 62443)
- Seeds 30 ISO 27001:2022 ISMS clause requirements (Clauses 4–10)
- Seeds 17 mandatory documented-information records (Clause 7.5) + sample interested parties (Clause 4.2)
- Seeds sample IS objectives (Clause 6.2) and KPI/KRI/KCI metrics (Clause 9.1)
- Seeds sample suppliers / third parties (Clauses 5.19–5.23)
- Seeds 5 sample workflow tasks (assigned to the first user)
- Seeds sample assessments (a control self-assessment + a vendor questionnaire)
- Backfills metric measurement history and historical posture snapshots (so trend charts render)
- Seeds sample security incidents (Clauses 5.24–5.28)
- Seeds sample awareness & training campaigns with participation records (Clauses 7.2/7.3)
- Creates 6 default RBAC roles
- Creates the first superuser account

---

## Local Development

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Start PostgreSQL (via Docker or local install)
docker compose up db -d

# Run the FastAPI server
DATABASE_URL=postgresql+asyncpg://grc:changeme@localhost:5432/itgrc \
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev  # Starts Vite dev server on http://localhost:5173
```

---

## Project Structure

```
IT-GRC/
├── backend/
│   ├── app/
│   │   ├── api/             # FastAPI route handlers
│   │   │   ├── auth.py      #   Authentication & user management
│   │   │   ├── controls.py  #   ISO 27001 Annex A controls CRUD
│   │   │   ├── clauses.py   #   ISMS clauses 4–10 conformity CRUD
│   │   │   ├── documents.py #   Documented information register (7.5)
│   │   │   ├── interested_parties.py # Interested parties register (4.2)
│   │   │   ├── objectives.py #   IS objectives register (6.2)
│   │   │   ├── metrics.py   #   KPI/KRI/KCI metrics (9.1)
│   │   │   ├── suppliers.py #   Supplier / third-party register (5.19–5.23)
│   │   │   ├── incidents.py #   Security incident register (5.24–5.28)
│   │   │   ├── training.py  #   Awareness & training (7.2/7.3)
│   │   │   ├── tasks.py     #   Cross-cutting workflow / task & approval engine
│   │   │   ├── analytics.py #   Risk heat map, posture trend, framework coverage
│   │   │   ├── assessments.py #  CSA / maturity / vendor questionnaires
│   │   │   ├── risks.py     #   Risk register CRUD
│   │   │   ├── soa.py       #   Statement of Applicability
│   │   │   ├── evidence.py  #   Evidence upload/download
│   │   │   ├── audits.py    #   Audit & findings management
│   │   │   ├── policies.py  #   Policy management
│   │   │   ├── assets.py    #   Asset inventory
│   │   │   ├── dashboard.py #   Dashboard statistics
│   │   │   └── deps.py      #   Shared dependencies (auth, DB)
│   │   ├── models/          # SQLAlchemy ORM models
│   │   ├── schemas/         # Pydantic request/response schemas
│   │   ├── seed/            # ISO 27001 controls + RBAC seed data
│   │   ├── config.py        # Application settings
│   │   ├── database.py      # Async SQLAlchemy engine
│   │   └── main.py          # FastAPI app with lifespan
│   ├── alembic/             # Database migrations
│   ├── uploads/             # Evidence file storage
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/           # Route page components
│   │   ├── services/        # API client functions
│   │   ├── hooks/           # React hooks (auth, etc.)
│   │   ├── types/           # TypeScript interfaces
│   │   └── App.tsx          # Root component with routing
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## ISO 27001:2022 Annex A Coverage

| Theme | Controls | Clause Range |
|-------|----------|-------------|
| **Organizational** | 37 | A.5.1 – A.5.37 |
| **People** | 8 | A.6.1 – A.6.8 |
| **Physical** | 14 | A.7.1 – A.7.14 |
| **Technological** | 34 | A.8.1 – A.8.34 |
| **Total** | **93** | |

---

## ISO/IEC 27019:2024 Energy-Sector Coverage

ISO/IEC 27019:2024 extends ISO/IEC 27002:2022 for **process control systems (SCADA/ICS) in the energy utility industry**. It reuses the Annex A controls above (adding energy-specific guidance) and introduces **12 sector-specific "ENR" controls** — the only controls it adds beyond Annex A. These are loaded as a distinct, filterable framework (`ISO 27019:2024`) that energy-sector organizations can adopt in addition to the base set. Wording is paraphrased for the app, not reproduced from the standard.

| Theme | Controls | Clauses |
|-------|----------|---------|
| **Organizational** | 2 | ENR.5.38 – ENR.5.39 |
| **Physical** | 4 | ENR.7.15 – ENR.7.18 |
| **Technological** | 6 | ENR.8.35 – ENR.8.40 |
| **Total** | **12** | |

> ENR.5.38 Identification of risks related to external business partners · ENR.5.39 Addressing security when dealing with customers · ENR.7.15 Securing control centres · ENR.7.16 Securing equipment rooms · ENR.7.17 Securing peripheral sites · ENR.7.18 Interconnected control and communication systems · ENR.8.35 Treatment of legacy systems · ENR.8.36 Integrity and availability of safety functions · ENR.8.37 Securing process control data communication · ENR.8.38 Logical connection of external process control systems · ENR.8.39 Least functionality · ENR.8.40 Emergency communication

---

## Additional Frameworks & Crosswalk

Beyond ISO 27001/27019, the portal ships **NIST CSF 2.0**, **SOC 2** and
**ISA/IEC 62443-2-1:2024** control catalogs so one control set can be mapped across
standards. Wording is paraphrased, not reproduced from the source frameworks.

| Framework | Granularity | Entries |
|-----------|-------------|---------|
| **NIST CSF 2.0** | Functions → Categories (Govern, Identify, Protect, Detect, Respond, Recover) | 22 |
| **SOC 2 (Trust Services Criteria)** | Common Criteria CC1–CC9 + Availability / Confidentiality / Processing Integrity / Privacy | 13 |
| **ISA/IEC 62443-2-1:2024** (OT / IACS) | 8 Security Program Elements — ORG, CM, NET, COMP, DATA, USER, EVENT, AVAIL | 8 |

Map controls across frameworks from any control's **Framework Crosswalk** section; the
**Frameworks** page shows a cross-framework coverage matrix. Starter crosswalks are
seeded: ISO 27001 ↔ CSF, ISO 27001 ↔ SOC 2, and **ISO 27001/27019 ↔ IEC 62443** (66
OT-mappings aligning each Annex A / ENR control with the 62443 program element it
supports — the IT-ISMS ↔ OT-program bridge from the ISAGCA & Secura combined-approach
white papers).

---

## ISO 27001:2022 Clauses 4–10 Coverage

The mandatory management-system requirements an organization is certified against
(distinct from the Annex A controls). All 30 are pre-loaded and tracked for conformity.

| Section | Requirements | Clauses |
|---------|-------------|---------|
| **4 Context of the organization** | 4 | 4.1 – 4.4 |
| **5 Leadership** | 3 | 5.1 – 5.3 |
| **6 Planning** | 5 | 6.1.1, 6.1.2, 6.1.3, 6.2, 6.3 |
| **7 Support** | 7 | 7.1 – 7.4, 7.5.1 – 7.5.3 |
| **8 Operation** | 3 | 8.1 – 8.3 |
| **9 Performance evaluation** | 6 | 9.1, 9.2.1, 9.2.2, 9.3.1 – 9.3.3 |
| **10 Improvement** | 2 | 10.1, 10.2 |
| **Total** | **30** | |

> Requirement text in the app is paraphrased for tracking purposes. ISO/IEC 27001:2022 is the authoritative source for the normative wording.

---

## RBAC Roles

| Role | Permissions |
|------|-----------|
| **CISO** | Full access to all modules |
| **GRC Manager** | Manage controls, risks, audits, policies, SoA, assets, evidence |
| **Risk Owner** | Manage assigned risks, read controls |
| **Control Owner** | Manage assigned controls, read risks, create evidence |
| **Auditor** | Manage audits and findings, read-only on all other modules |
| **Viewer** | Read-only access to all modules |

---

## API Documentation

Once running, interactive API documentation is available at:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

Key API endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/login` | Authenticate and get JWT token |
| GET | `/api/v1/auth/users` | List users (for assignee/owner pickers) |
| GET | `/api/v1/tasks` | List workflow tasks (filters: assignee, status, type, priority, overdue) |
| POST | `/api/v1/tasks/{id}/decision` | Record an approval/sign-off decision |
| GET | `/api/v1/analytics/risk-heatmap` | 5×5 risk heat map (inherent/residual) |
| GET | `/api/v1/analytics/posture-trend` | Posture score time series |
| GET | `/api/v1/analytics/framework-coverage` | Cross-framework crosswalk coverage matrix |
| GET/POST | `/api/v1/controls/{id}/mappings` | List / add cross-framework control mappings |
| GET/POST | `/api/v1/assessments` | Control self-assessments & vendor questionnaires |
| POST | `/api/v1/assessments/{id}/populate` | Generate items from a framework's controls |
| POST | `/api/v1/metrics/{id}/measurements` | Record a metric measurement (trend point) |
| GET | `/api/v1/controls` | List ISO 27001 Annex A controls |
| GET | `/api/v1/clauses` | List ISMS clause requirements (4–10) |
| GET | `/api/v1/documents` | List documented information (7.5) |
| GET | `/api/v1/interested-parties` | List interested parties (4.2) |
| GET | `/api/v1/objectives` | List IS objectives (6.2) |
| GET | `/api/v1/metrics` | List KPI/KRI/KCI metrics (9.1) |
| GET | `/api/v1/suppliers` | List suppliers / third parties (5.19–5.23) |
| GET | `/api/v1/incidents` | List security incidents (5.24–5.28) |
| GET | `/api/v1/training` | List awareness & training campaigns (7.2/7.3) |
| GET | `/api/v1/risks` | List risks |
| POST | `/api/v1/risks` | Create a new risk |
| GET | `/api/v1/soa` | List Statement of Applicability |
| POST | `/api/v1/evidence/upload` | Upload evidence file |
| GET | `/api/v1/audits` | List audits |
| GET | `/api/v1/policies` | List policies |
| GET | `/api/v1/assets` | List assets |
| GET | `/api/v1/dashboard/stats` | Dashboard statistics |

---

## IdP Integration

### SAML

Set in `.env`:
```
SAML_METADATA_URL=https://your-idp.com/metadata.xml
```

### OIDC

Set in `.env`:
```
OIDC_DISCOVERY_URL=https://your-idp.com/.well-known/openid-configuration
OIDC_CLIENT_ID=your-client-id
OIDC_CLIENT_SECRET=your-client-secret
```

---

## Database Migrations

Schema is managed by **Alembic**. The app runs `alembic upgrade head` automatically
on startup, so a fresh database is provisioned and existing ones are upgraded with
no manual step. To change the schema:

```bash
cd backend
# 1) edit the SQLAlchemy models, then autogenerate a migration
alembic revision --autogenerate -m "describe your change"
# 2) review the generated file in alembic/versions/, then apply it
alembic upgrade head
```

The baseline migration (`0001_baseline`) builds the full schema from the models'
metadata; every subsequent change should be an autogenerated revision.

## Testing & CI

```bash
# Backend unit tests (no database required)
cd backend
pip install -r requirements-dev.txt
python -m pytest -q

# Frontend type-check + production build
cd frontend
npm run build
```

GitHub Actions ([`.github/workflows/ci.yml`](.github/workflows/ci.yml)) runs on every push and pull request:
- **Backend** — byte-compiles the app and runs the pytest unit suite (RAG metric logic, 5×5 risk scoring, seed-data integrity)
- **Migrations** — spins up Postgres and runs `alembic upgrade head → downgrade base → upgrade head`, then `alembic check` to confirm the schema matches the models
- **Frontend** — runs `tsc && vite build` to type-check and build the entire React app

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## Disclaimer

This tool assists with ISO 27001:2022 compliance management but does **not** guarantee certification. Certification requires an accredited external audit. Use this portal to organize your ISMS, track controls, manage risks, and prepare for audits — but always engage qualified auditors for the formal certification process.
