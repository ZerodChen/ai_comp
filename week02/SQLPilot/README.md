# SQLPilot (Week 2: Foundation)

This project is an intelligent helper tool that allows users to query databases using both Natural Language and raw SQL.

## Project Structure

- `backend/`: FastAPI application (Python)
- `frontend/`: Vue 3 application (Node.js)
- `db-test/`: Test database initialization scripts (e.g., PostgreSQL).

## Phase 1: Foundation & Connectivity (Implemented)

We have established the backend infrastructure, including:
- **FastAPI Setup**: Core app structure with configuration.
- **Metadata Store**: SQLite database managed by Alembic migrations.
- **Connection Management**: APIs to add/list database connections.
- **Metadata Indexer**: Automatic schema extraction (tables/columns) from connected databases (Postgres/SQLite).

## Setup Instructions

### Prerequisites
- Python 3.13+
- Node.js 22+

### Backend Setup

1. **Navigate to backend**:
   ```bash
   cd week02/SQLPilot/backend
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Mac/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r ../../../requirements.txt
   ```

4. **Initialize Database**:
   ```bash
   alembic upgrade head
   ```

5. **Start Server**:
   ```bash
   uvicorn app.main:app --reload
   ```

## Verification (Phase 1)

1. **Start the server** (step 5 above).

2. **Add a Test Connection** (using the local metadata DB itself):
   ```powershell
   Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/connections/" -Method Post -ContentType "application/json" -Body '{"name": "Self Metadata", "db_type": "sqlite", "connection_url": "sqlite:///./metadata.db"}'
   ```

3. **Verify Indexing**:
   ```powershell
   Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/connections/1/schema" -Method Get
   ```
   You should see a JSON list of tables (`db_connections`, `table_metadata`) and their columns.

## Testing

To run the backend test suite:

```bash
cd week02/SQLPilot/backend
pytest
```

## Deployment

To run the full stack using Docker Compose:

```bash
cd week02/SQLPilot
docker-compose up --build
```

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000

## Test Database

A PostgreSQL database with sample data is included in the Docker Compose setup for testing purposes.

- **Host**: `localhost` (or `db-test-pg` inside docker network)
- **Port**: `5432`
- **User**: `testuser`
- **Password**: `testpassword`
- **Database**: `testdb`

You can connect to this database using the tool to test schema indexing and querying.

| Environment | Connection URL |
| :--- | :--- |
| **Running Locally** (Development) | `postgresql://testuser:testpassword@localhost:5432/testdb` |
| **Running in Docker** (Compose) | `postgresql://testuser:testpassword@db-test-pg:5432/testdb` |

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
