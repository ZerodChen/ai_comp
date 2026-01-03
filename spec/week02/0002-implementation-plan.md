# Week 02 Implementation Plan

This document outlines the step-by-step implementation plan for the **AI-Powered Database Query Tool**. The project is divided into 4 distinct phases to ensure steady progress and clear deliverables.

### Prerequisites
- Python 3.13+
- Node.js 22+
- Docker & Docker Compose (optional)

## Phase 1: Foundation & Connectivity
**Goal**: Establish the backend infrastructure and enable database connection management with metadata indexing.
**Timeline**: Days 1-2

### Tasks
1.  **Project Initialization**
    *   [ ] Set up `week02/backend` structure (FastAPI, Alembic, SQLAlchemy).
    *   [ ] Set up `week02/frontend` structure (Vue 3, Vite, Element Plus).
    *   [ ] Configure root `package.json` workspaces and `requirements.txt`.

2.  **Metadata Store Implementation**
    *   [ ] Define SQLAlchemy models for `DBConnection`, `TableMetadata`, and `ColumnMetadata`.
    *   [ ] Create Alembic migrations to initialize the SQLite metadata store.

3.  **Connection Management API**
    *   [ ] Implement `POST /api/connections` to save encrypted connection details.
    *   [ ] Implement `GET /api/connections` to list saved connections.
    *   [ ] Implement `GET /api/connections/{id}` to retrieve details.

4. **Metadata Indexer Service**
    *   [ ] Implement `MetadataService` to connect to a target DB (Focus on **PostgreSQL** for MVP) using SQLAlchemy inspection.
    *   [ ] Extract table names, column names, and types.
    *   [ ] Save extracted schema to the local SQLite metadata store.
    *   [ ] Trigger indexing automatically upon connection creation.

### Deliverables
*   Functional Backend API for managing connections.
*   Ability to connect to a real database and cache its schema locally.
*   A populated SQLite metadata database.

### Verification
1.  **Start Server**: `uvicorn app.main:app --reload`
2.  **Add Connection**: Use Swagger UI (`/docs`) to POST a valid Postgres URI.
3.  **Check DB**: Inspect local SQLite db to verify `table_metadata` contains entries matching the Postgres schema.

---

## Phase 2: Query Engine Core
**Goal**: Implement the core logic for executing SQL and translating Natural Language to SQL.
**Timeline**: Days 2-3

### Tasks
1.  **SQL Execution Service**
    *   [ ] Implement `QueryService.execute_sql(connection_id, sql)`.
    *   [ ] Connect to the target database dynamically.
    *   [ ] Execute the query and return results as a list of dictionaries.
    *   [ ] Handle connection errors and query syntax errors gracefully.

2.  **Security & Validation**
    *   [ ] Integrate `sqlglot` or `sqlparse`.
    *   [ ] Implement a validation step to detect and block destructive commands (`DROP`, `DELETE`, `TRUNCATE`, `ALTER`).
    *   [ ] Add a configuration flag to enable/disable read-only mode.

3.  **LLM Integration (NL to SQL)**
    *   [ ] Set up `LLMService` to communicate with OpenAI API (or local mock).
    *   [ ] Design the System Prompt:
        *   Include schema context (tables/columns) from the metadata store.
        *   Add instructions for SQL dialect (Postgres vs MySQL).
    *   [ ] Implement `POST /api/query/natural-language`.
    *   [ ] Parse LLM response to extract just the SQL code.

### Deliverables
*   API endpoint that accepts raw SQL and returns data (safely).
*   API endpoint that accepts a natural language question and returns valid SQL + Data.

### Verification
1.  **Test SQL**: `POST /api/query/sql` with `{"sql": "SELECT 1"}` -> Returns `[{"?column?": 1}]`.
2.  **Test Security**: `POST /api/query/sql` with `{"sql": "DROP TABLE users"}` -> Returns `403 Forbidden`.
3.  **Test NL**: `POST /api/query/natural-language` with `{"question": "list all tables"}` -> Returns generated SQL and data.

---

## Phase 3: Frontend & UI Integration
**Goal**: Build the user interface and connect it to the backend services.
**Timeline**: Days 3-4

### Tasks
1.  **Layout Implementation**
    *   [ ] Create the "IDE Layout" (3-column structure: Sidebar, Main, Right Panel).
    *   [ ] Create the "Dashboard Layout" (Card grid structure).
    *   [ ] Implement a global state (Pinia) to manage the active layout mode (`isIdeMode`).

2.  **Connection Management UI**
    *   [ ] Build the "Connection List" sidebar component.
    *   [ ] Build the "Create Connection" modal form.
    *   [ ] Connect to `POST /api/connections` and refresh list on success.

3.  **Query Interface UI**
    *   [ ] Build the "Natural Language Input" component.
    *   [ ] Build the "SQL Editor" component (using a code editor library like `monaco-editor` or simple textarea).
    *   [ ] Build the "Schema Browser" tree view in the right sidebar.
    *   [ ] Build the "Results Table" component with pagination.

4.  **Integration**
    *   [ ] Wire up the "Run Query" button to the backend APIs.
    *   [ ] Display loading states while fetching data or calling LLM.
    *   [ ] Handle and display error messages (e.g., "Invalid SQL").

### Deliverables
*   A fully functional web application where users can add connections, browse schema, and run queries.
*   Two switchable UI modes (IDE vs Dashboard).

### Verification
1.  **Launch Frontend**: `npm run dev` and open `http://localhost:5173`.
2.  **Add Connection**: Click "+ New Connection" -> Fill form -> See new item in sidebar.
3.  **Browse Schema**: Expand a table in the Right Sidebar -> See columns.
4.  **Run Query**: Type "Show me users" -> Click Run -> See table results.
5.  **Switch Mode**: Click "View: IDE/Dashboard" -> Confirm layout changes completely.

---

## Phase 4: Polish & Advanced Features
**Goal**: Refine the user experience, add export capabilities, and prepare for deployment.
**Timeline**: Days 4-5

### Tasks
1.  **Result Export**
    *   [ ] Implement backend utility to convert result sets to CSV/JSON strings.
    *   [ ] Add "Export" button in the frontend Results panel.
    *   [ ] Trigger browser download for the generated file.

2.  **Testing**
    *   [ ] Write unit tests for `ConnectionService` (password encryption, storage).
    *   [ ] Write unit tests for `QueryService` (security validation logic).
    *   [ ] Write integration tests for the full NL-to-SQL flow (mocking the LLM).
    *   [ ] Ensure test coverage > 90%.

3.  **Deployment Prep**
    *   [ ] Create `Dockerfile` for Backend.
    *   [ ] Create `Dockerfile` for Frontend (multi-stage build).
    *   [ ] Create `docker-compose.yml` for easy local orchestration.
    *   [ ] Document environment variables (`OPENAI_API_KEY`, `DATABASE_URL`).

### Deliverables
*   Production-ready Docker configuration.
*   Export functionality.
*   Comprehensive test suite.
*   Final documentation update.

### Verification
1.  **Export**: Run a query -> Click "Export CSV" -> Verify file downloads and opens correctly.
2.  **Tests**: Run `pytest --cov=app` -> Verify passing tests and >90% coverage report.
3.  **Docker**: Run `docker-compose up` -> Verify app is accessible at `http://localhost:5173` and API at `http://localhost:8000`.
