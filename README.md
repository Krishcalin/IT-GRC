# IT-GRC Portal — ISO 27001:2022

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)](https://react.dev)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)](https://postgresql.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![ISO 27001](https://img.shields.io/badge/ISO_27001-2022-blue)](https://www.iso.org/standard/27001)
[![Controls](https://img.shields.io/badge/Annex_A_Controls-93-orange)](#controls-library)
[![ISMS Clauses](https://img.shields.io/badge/ISMS_Clauses_4--10-30-9cf)](#isms-clause-conformity-clauses-410)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](#quick-start)

An **open-source IT Governance, Risk & Compliance (GRC) portal** purpose-built for **ISO 27001:2022** certification management. Clone it, deploy internally with Docker Compose, integrate with your corporate IdP (SAML/OIDC), and start managing your ISMS.

---

## Features

### Controls Library
- All **93 Annex A controls** from ISO 27001:2022 pre-loaded and categorized by theme
- 4 themes: Organizational (37), People (8), Physical (14), Technological (34)
- Track implementation status, assign owners, set review dates
- Link controls to risks, evidence, and audit findings

### ISMS Clause Conformity (Clauses 4–10)
- All **30 mandatory management-system requirements** from ISO 27001:2022 Clauses 4–10 pre-loaded
- Organized by section: Context, Leadership, Planning, Support, Operation, Performance evaluation, Improvement
- Track conformity status (Not Assessed → In Progress → Partially Conformant → Conformant / Nonconformant), assign owners, set review dates
- Each clause flags the **mandatory documented information** it requires (scope, policy, SoA, objectives, audit/management-review records, etc.)
- Distinct from Annex A controls — per Clause 1 (Scope), these clauses cannot be excluded when claiming conformity

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
- Creates all database tables
- Seeds 93 ISO 27001:2022 Annex A controls
- Seeds 30 ISO 27001:2022 ISMS clause requirements (Clauses 4–10)
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
| GET | `/api/v1/controls` | List ISO 27001 Annex A controls |
| GET | `/api/v1/clauses` | List ISMS clause requirements (4–10) |
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
