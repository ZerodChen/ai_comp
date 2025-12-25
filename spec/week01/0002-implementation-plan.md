# Ticket Management Tool - Implementation Plan

## 1. Phase 1: Project Initialization & Setup
**Goal**: Set up the project structure, development environment, and basic configurations for both backend and frontend.

### 1.1 Root & Directory Structure
- [x] Create project root directory.
- [x] Initialize Git repository.
- [x] Create `README.md` and `.gitignore` (Python + Node).
- [x] Create `docker-compose.yml` for PostgreSQL and optional full-stack running.

### 1.2 Backend Initialization (FastAPI)
- [x] Create `backend/` directory.
- [x] Set up Python virtual environment (`venv`).
- [x] Create `requirements.txt` (FastAPI, Uvicorn, SQLAlchemy, AsyncPG, Pydantic, Alembic, python-dotenv).
- [x] Create basic FastAPI app structure:
    - `app/main.py`: Entry point with `Hello World` endpoint.
    - `app/core/config.py`: Configuration loading (Env vars).
- [x] Verify server runs (`uvicorn app.main:app --reload`).

### 1.3 Database Setup
- [x] Set up PostgreSQL container via `docker-compose.yml`.
- [x] Initialize Alembic (`alembic init alembic`).
- [x] Configure `alembic.ini` and `env.py` to use async driver and load config.

### 1.4 Frontend Initialization (Vue 3 + Vite)
- [x] Create `frontend/` directory using `npm create vite@latest` (Vue, JavaScript/TypeScript).
- [x] Install dependencies: `npm install`.
- [x] Install additional libraries: `element-plus`, `axios`, `pinia`, `vue-router`, `sass`.
- [x] Configure `vite.config.js` (proxy for API).
- [x] Verify frontend runs (`npm run dev`).

## 2. Phase 2: Backend Implementation - Core & Database
**Goal**: Implement database models, migrations, and core application logic.

### 2.1 Database Models
- [x] Define SQLAlchemy Base in `app/db/base.py`.
- [x] Implement `Tag` model in `app/models/tag.py`:
    - `id` (PK), `name` (Unique).
- [x] Implement `Ticket` model in `app/models/ticket.py`:
    - `id` (PK), `title`, `description`, `created_at`, `updated_at`.
- [x] Implement `ticket_tags` association table.
- [x] Update `app/db/base.py` to import all models.

### 2.2 Migrations
- [x] Generate initial migration: `alembic revision --autogenerate -m "Initial tables"`.
- [x] Apply migration: `alembic upgrade head`.

### 2.3 Pydantic Schemas
- [x] Create `app/schemas/tag.py`: `TagBase`, `TagCreate`, `TagResponse`.
- [x] Create `app/schemas/ticket.py`: `TicketBase`, `TicketCreate`, `TicketUpdate`, `TicketResponse`.

## 3. Phase 3: Backend Implementation - API Endpoints
**Goal**: Implement RESTful APIs for Tags and Tickets.

### 3.1 Tags API
- [x] Implement CRUD endpoints in `app/api/endpoints/tags.py`:
    - `POST /`: Create tag.
    - `GET /`: List all tags.
    - `PUT /{id}`: Update tag.
    - `DELETE /{id}`: Delete tag.
    - `DELETE /batch`: Batch delete tags.
- [x] Register router in `app/api/api.py`.

### 3.2 Tickets API
- [x] Implement CRUD endpoints in `app/api/endpoints/tickets.py`:
    - `POST /`: Create ticket (with tags).
    - `GET /`: List tickets (Pagination, Search `q`, Filter `tag_id`).
    - `GET /{id}`: Get ticket details.
    - `PUT /{id}`: Update ticket (content & tags).
    - `DELETE /{id}`: Delete ticket.
    - `DELETE /batch`: Batch delete tickets.
- [x] Register router in `app/api/api.py`.

### 3.3 Unit Testing
- [x] Install `pytest` and `httpx`.
- [x] Configure `conftest.py` for async DB testing.
- [x] Write tests for Tag CRUD.
- [x] Write tests for Ticket CRUD and Filters.
- [x] Run tests and ensure all pass.

## 4. Phase 4: Frontend Implementation - Basics
**Goal**: Set up frontend structure, routing, and shared components.

### 4.1 Project Structure & Routing
- [x] Setup Vue Router in `src/router/index.js`.
- [x] Create placeholder views: `TicketView.vue`, `TagView.vue`.
- [x] Configure App layout (Navigation/Header) in `App.vue`.

### 4.2 API Client
- [x] Setup Axios instance in `src/api/request.js` (Base URL, Interceptors).
- [x] Create API service modules:
    - `src/api/tags.js`
    - `src/api/tickets.js`

## 5. Phase 5: Frontend Implementation - Features
**Goal**: Build the UI for Ticket and Tag management.

### 5.1 Tag Management View
- [x] Implement `TagView.vue`:
    - Table to list tags.
    - "New Tag" button opening a Modal.
    - "Edit" button opening a Modal with data.
    - "Delete" button with confirmation.
    - "Batch Delete" support (checkboxes).
- [x] Integrate with `src/api/tags.js`.

### 5.2 Ticket Management View - List
- [x] Implement `TicketView.vue` List area:
    - Search input.
    - Tag filter dropdown.
    - Table to list tickets (Title, Badges for Tags, Actions).
    - Pagination component.
- [x] Integrate fetching logic with params (page, size, q, tag_id).

### 5.3 Ticket Management View - Create/Edit
- [x] Create `TicketDialog.vue` component:
    - Form with Title (Input), Description (Textarea).
    - Tag selector (Multi-select) fetching available tags.
- [x] Integrate Create/Update API calls.
- [x] Implement Delete and Batch Delete actions.

## 6. Phase 6: Final Polish & Delivery
**Goal**: Verify functionality, clean up code, and document.

### 6.1 Testing & Validation
- [x] Manual E2E testing of all features.
- [x] Check edge cases (empty states, long text, network errors).
- [x] Verify Docker Compose startup.

### 6.2 UI Polish
- [x] Ensure Element Plus styles are consistent.
- [x] Add loading states (spinners) during API calls.
- [x] Add toast notifications for success/error actions.

### 6.3 Documentation
- [ ] Update `README.md` with setup instructions (referencing `0001-instructions.md`).
