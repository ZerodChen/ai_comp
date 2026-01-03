# Week 02: AI-Powered Database Query Tool - Detailed Requirements & Design

## 1. Project Overview
This project is an intelligent database helper tool that allows users to query databases using both Natural Language (NL) and raw SQL. It simplifies database interactions by automatically indexing metadata and leveraging Large Language Models (LLMs) to translate human questions into executable SQL queries.

### Core Value Proposition
- **Accessibility**: Enable non-technical users to query complex databases.
- **Efficiency**: Speed up query writing for developers.
- **Safety**: Validate queries before execution.

## 2. Functional Requirements

### 2.1 Database Connection & Management
- **Add Connection**: User provides a database connection string (URI).
- **Supported Databases**:
  - **Phase 1 (MVP)**: PostgreSQL (Primary focus).
  - **Future**: MySQL, SQLite, BigQuery, MongoDB.
- **Metadata Indexing**: Upon connection, the system automatically fetches:
  - Table/View names
  - Column names and types
  - Foreign key relationships
  - (Optional) Sample data for context
- **Metadata Storage**: Metadata is cached locally (SQLite) to avoid repeated costly fetching.
- **Connection List**: View saved database connections.

### 2.2 Natural Language Query (NLQ)
- **Input**: User types a question in plain English (e.g., "Show me top 5 users by sales").
- **Processing**:
  1. Retrieve relevant schema metadata.
  2. Construct prompt for LLM.
  3. Call LLM API (OpenAI or Local) to generate SQL.
- **Output**: Display the generated SQL and the query result.

### 2.3 SQL Query Mode
- **Input**: User types raw SQL.
- **Validation**:
  - Syntax checking.
  - Security check (prevent dangerous operations like `DROP`, `DELETE` if configured as read-only).
- **Execution**: Run query against the target database.

### 2.4 Result Management
- **Display**: Render results in a paginated data table, if no limit provided in the sql, then by default make it 1000.
- **Export**: Download results as CSV or JSON.

## 3. Technical Design

### 3.1 Architecture
- **Frontend**: Vue.js 3 + Element Plus (Single Page Application).
- **Backend**: FastAPI (Python) serving REST APIs.
- **Metadata Store**: SQLite database managed by the backend.
- **AI Engine**: Service layer connecting to OpenAI API or local HuggingFace models.

### 3.2 Backend Stack
- **Framework**: FastAPI
- **ORM**: SQLAlchemy (Async)
- **Migrations**: Alembic
- **Validation**: Pydantic v2
- **SQL Parsing**: `sqlglot` or `sqlparse` for basic validation.

### 3.3 Database Schema (Metadata Store)
We need to store connection details and cached schemas.

```mermaid
erDiagram
    DBConnection ||--o{ TableMetadata : contains
    TableMetadata ||--o{ ColumnMetadata : has

    DBConnection {
        int id PK
        string name
        string db_type "postgres (MVP) / mysql / sqlite"
        string connection_url "Encrypted"
        datetime created_at
    }

    TableMetadata {
        int id PK
        int connection_id FK
        string table_name
        string description
    }

    ColumnMetadata {
        int id PK
        int table_id FK
        string column_name
        string data_type
        boolean is_primary_key
        boolean is_foreign_key
    }
```

## 4. API Design

### 4.1 Connection Management
- `POST /api/connections`: Create a new DB connection and trigger indexing.
- `GET /api/connections`: List available connections.
- `GET /api/connections/{id}/schema`: Get cached schema for a connection.

### 4.2 Query Execution
- `POST /api/query/natural-language`:
  - Body: `{ "connection_id": 1, "question": "..." }`
  - Response: `{ "sql": "SELECT ...", "data": [...], "error": null }`
- `POST /api/query/sql`:
  - Body: `{ "connection_id": 1, "sql": "SELECT ..." }`
  - Response: `{ "data": [...], "error": null }`

## 5. UI Design Preview

The application supports **two distinct layout modes**, switchable via a toggle in the top navigation bar. This allows users to choose between a focused, navigation-driven experience and a dense, high-context workspace.

### 5.1 Mode A: IDE View (Integrated Workspace)
*Best for: Power users, frequent context switching, and managing multiple DBs.*

- **Layout**: 3-column "IDE-style" layout.
- **Header**: Branding & "View Switcher" (Toggle to Dashboard Mode).
- **Left Sidebar**: Connection List (Click to switch DB instantly) + "New Connection".
- **Middle Area**: Query Input (NL/SQL) & Results.
- **Right Sidebar**: Schema Browser.

```
+-----------------------------------------------------------------------------------------------+
|  [ AI DB Helper ]          [ View: IDE / Dashboard ]                                          |
+----------------------+----------------------------------------------+-------------------------+
| [ + New Connection ] |  [ Natural Language ]  [ SQL Editor ]        |  Schema Browser         |
|                      |                                              |                         |
| Connections:         |  Ask a question:                             |  > public               |
|                      |  [ Show me top users by sales...          ]  |  v tables               |
| [ PG: Production   ] |  [________________________________________]  |    > users              |
| (Active)             |             [ Run Query ]                    |    v orders             |
|                      |                                              |      - id (int)         |
| [ MY: Analytics    ] |  ------------------------------------------  |      - user_id (fk)     |
|                      |  Generated SQL:                              |      - amount (dec)     |
| [ SQ: Local Dev    ] |  SELECT * FROM users...                      |      - status (str)     |
|                      |  ------------------------------------------  |                         |
|                      |                                              |                         |
|                      |  Query Results:             [ Export CSV v ] |                         |
|                      |  +------------+------------+                 |                         |
|                      |  | Name       | Sales      |                 |                         |
|                      |  +------------+------------+                 |                         |
|                      |  | Alice      | 1000.50    |                 |                         |
|                      |  | Bob        | 850.00     |                 |                         |
|                      |  | ...        | ...        |                 |                         |
|                      |  +------------+------------+                 |                         |
|                      |                                              |                         |
+----------------------+----------------------------------------------+-------------------------+
```

### 5.2 Mode B: Dashboard View (Focus Mode)
*Best for: Single-task focus, smaller screens, or presentation.*

- **Dashboard Page**: Card grid of all connections.
- **Query Page**: Full-screen focus on the active database query.
- **Navigation**: User must click "Back" to return to the dashboard.

**Screen 1: The Dashboard**
```
+-----------------------------------------------------------------------+
|  AI DB Helper              [ View: IDE / Dashboard ]                  |
+-----------------------------------------------------------------------+
|  [ + New Connection ]                                                 |
|                                                                       |
|  Saved Connections:                                                   |
|  +------------------+  +------------------+  +------------------+     |
|  | [PG] Production  |  | [MY] Analytics   |  | [SQ] Local Dev   |     |
|  |                  |  |                  |  |                  |     |
|  | Host: 10.0.0.5   |  | Host: aws-rds... |  | File: ./dev.db   |     |
|  | Last: 2 mins ago |  | Last: 1 day ago  |  | Last: Never      |     |
|  | [Query] [Edit]   |  | [Query] [Edit]   |  | [Query] [Edit]   |     |
|  +------------------+  +------------------+  +------------------+     |
+-----------------------------------------------------------------------+
```

**Screen 2: The Query Interface (Focus)**
```
+-----------------------------------------------------------------------+
|  [< Back]  Production DB (Postgres)               [ Export CSV v ]    |
+-----------------------------------------------------------------------+
| Schema Browser |  [ Natural Language ]  [ SQL Editor ]                |
| (Collapsible)  |                                                      |
|                |  Ask a question about your data:                     |
| > users        |  [ Show me the top 5 customers by total order val ]  |
| v orders       |  [________________________________________________]  |
|   - id         |                                                      |
|   - amount     |             [ Generate & Run SQL ]                   |
|                |                                                      |
|                |  Results:                                            |
|                |  +--------------+--------------+                     |
|                |  | Name         | Total        |                     |
|                |  +--------------+--------------+                     |
|                |  | Alice Smith  | $12,450.00   |                     |
|                |  +--------------+--------------+                     |
+----------------+------------------------------------------------------+
```

### 5.3 Create Connection Modal
Triggered by the "+ New Connection" button in either mode.

```
+-------------------------------------------+
|  Connect to Database                  [X] |
+-------------------------------------------+
|  Connection Name:                         |
|  [ Production DB _______________________] |
|                                           |
|  Database Type:                           |
|  (o) PostgreSQL  ( ) MySQL  ( ) SQLite    |
|  (MySQL/SQLite coming soon)               |
|                                           |
|  Connection URL:                          |
|  [ postgresql://user:pass@localhost:5432] |
|                                           |
|  (Optional) User/Pass override if needed  |
|                                           |
|                  [ Cancel ]  [ Connect ]  |
+-------------------------------------------+
```

## 6. Unit Test Strategy

We will use `pytest` for backend testing and also make sure test coverage meet 90% or above.

### 6.1 Key Test Cases

#### Connection Service
- `test_create_connection_success`: Verify DB connection is saved and password encrypted.
- `test_connect_invalid_url`: Verify system handles unreachable DBs gracefully.

#### Metadata Indexer
- `test_fetch_metadata`: Mock a DB engine and verify tables/columns are correctly parsed into `TableMetadata` models.

#### Query Engine
- `test_sql_validation_safe`: Verify `SELECT *` passes.
- `test_sql_validation_unsafe`: Verify `DROP TABLE` raises `SecurityException`.
- `test_nl_to_sql_prompt_generation`: Verify prompt includes schema context.

## 7. Local Environment Setup

### 7.1 Prerequisites
- Python 3.13+
- Node.js 22+
- Docker & Docker Compose (optional)

### 7.2 Backend Setup
```bash
cd week2/backend
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env       # Configure OPENAI_API_KEY
alembic upgrade head       # Initialize metadata store
uvicorn app.main:app --reload
```

### 7.3 Frontend Setup
```bash
cd week2/frontend
npm install
npm run dev
```

## 8. Deployment Instructions

### 8.1 Local Development (Docker Compose)
A `docker-compose.yml` will be provided to spin up both frontend and backend.

```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    env_file: .env
    volumes:
      - ./backend:/app

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    depends_on:
      - backend
```

### 8.2 Production Deployment
1.  **Containerization**: Build optimized Docker images (multi-stage builds).
    - Frontend: Build static assets and serve via Nginx.
    - Backend: Gunicorn + Uvicorn workers.
2.  **Orchestration**: Deploy to Kubernetes or AWS ECS.
3.  **Security**:
    - Inject secrets (DB URLs, API Keys) via environment variables.
    - Enable HTTPS.
    - Set up a read-only DB user for the tool to minimize risk.
