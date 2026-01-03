# Week 2: AI-Powered Database Query Tool

This project is an intelligent helper tool that allows users to query databases using both Natural Language and raw SQL.

## Project Structure

- `backend/`: FastAPI application (Python)
- `frontend/`: Vue 3 application (Node.js)

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
   cd week02/backend
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
   pip install -r requirements.txt
   ```
   *(Note: Ensure `requirements.txt` exists in root or `week02/backend`)*

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

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
