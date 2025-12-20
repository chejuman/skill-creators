---
name: fullstack-query-builder
description: Transform PostgreSQL queries into complete full-stack applications with React + shadcn/ui frontend and FastAPI backend. Use when user provides SQL query and wants automated UI design, component generation, API implementation, and full monorepo deployment. Triggers on "build app from query", "query to application", "fullstack from SQL", or rapid prototyping of data-driven applications.
---

# Full-Stack Query Builder

Transform PostgreSQL queries into production-ready full-stack applications with intelligent UI design, React components, and FastAPI backend.

## When to Use This Skill

- User provides SQL query and wants complete application
- Rapidly prototype data-driven UIs from database queries
- Automate frontend-backend boilerplate for database-driven apps
- Build admin panels or dashboards from existing databases

## Prerequisites

- PostgreSQL database (local or remote)
- Node.js 18+ and npm
- Python 3.10+ and pip

## Phase-Based Workflow

### Phase 1: Database Query & Analysis

**Command:** `npx tsx scripts/cli.ts start`

Connect to PostgreSQL, execute query, analyze results, recommend UI type.

**Prompts:** Connection string, SQL query
**Output:** Row/column analysis, UI recommendation (table/cards/detail/dashboard)
**Approval:** "Continue with this data?"

### Phase 2: UI Design Expert Analysis

**Command:** `npx tsx scripts/cli.ts continue 2`

Generate UI design specification with component hierarchy.

**Prompts:** Resource name (e.g., "users")
**Output:** Main view, React components, shadcn/ui components, layout
**Approval:** "Approve design?"

### Phase 3: Frontend Implementation

**Command:** `npx tsx scripts/cli.ts continue 3`

Create Vite + React + TypeScript project with generated components.

**Prompts:** Project path (e.g., `./my-app`)
**Output:** Complete frontend at `{project}/frontend`
**Run:** `cd frontend && npm run dev`
**Approval:** "Frontend looks correct?"

### Phase 4: Backend API Design

**Command:** `npx tsx scripts/cli.ts continue 4`

Design RESTful API endpoints matching frontend needs.

**Output:** GET/POST/PUT/DELETE endpoints, Pydantic models
**Approval:** "Approve API design?"

### Phase 5: Backend Implementation

**Command:** `npx tsx scripts/cli.ts continue 5`

Create FastAPI project with routers and models.

**Output:** Complete backend at `{project}/backend`
**Run:** `cd backend && uvicorn app.main:app --reload`
**Approval:** "Backend works?"

### Phase 6: Full Integration

**Command:** `npx tsx scripts/cli.ts continue 6`

Connect frontend and backend with API client.

**Output:** Integrated monorepo with `.env` files and README

## Project Structure

```
my-app/
├── frontend/           # React + Vite + shadcn/ui
│   ├── src/
│   │   ├── components/
│   │   ├── lib/        # API client
│   │   ├── pages/
│   │   ├── store/      # Zustand
│   │   └── types/
│   └── .env
└── backend/            # FastAPI + PostgreSQL
    ├── app/
    │   ├── routers/    # API endpoints
    │   ├── models/     # SQLAlchemy
    │   └── schemas/    # Pydantic
    └── .env
```

## Workflow Commands

- **Status:** `npx tsx scripts/cli.ts status`
- **Continue:** `npx tsx scripts/cli.ts continue <2-6>`
- **Reset:** `npx tsx scripts/cli.ts reset`

## Configuration

**Frontend (.env):**
```
VITE_API_URL=http://localhost:8000
```

**Backend (.env):**
```
DATABASE_URL=postgresql://user:pass@host:5432/db
CORS_ORIGINS=http://localhost:5173
```

## Running Application

**Terminal 1:** `cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload`
**Terminal 2:** `cd frontend && npm install && npm run dev`

Backend: http://localhost:8000
Frontend: http://localhost:5173

## Troubleshooting

- **Connection failed:** Verify PostgreSQL running, check connection format
- **Query validation:** Only SELECT queries allowed for security
- **Large results:** Pagination auto-added for >50 rows
- **Complex JOINs:** Start simple, add complexity after generation

## Resources

- `references/ui-type-mapping.md` - UI type decision tree
- Component templates in `assets/components/`

**Tech Stack:** React 18, Vite 5, TypeScript, shadcn/ui, FastAPI, PostgreSQL, SQLAlchemy
