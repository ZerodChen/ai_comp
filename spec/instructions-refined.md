# AI Development Lifecycle Guide

This document outlines the standard workflow for AI-assisted development, ensuring structured progression from idea to delivery. It is divided into 5 key stages: **Idea & Research**, **Requirements & Design**, **Implementation Planning**, **Development**, and **Verification & Delivery**.

---

## 1. Idea & Research (Deep Exploration)
**Goal:** Clarify the concept, gather context, and explore technical possibilities.

### Activities:
- **Idea Formulation**: Describe the core problem and high-level solution.
- **Deep Research**: Use the `Search` tool to explore:
  - Existing codebase patterns.
  - Third-party libraries (check latest stable versions).
  - Security best practices (e.g., non-root containers, secret management).
- **AI Interaction**: Brainstorm with the AI to refine the scope.

### Output:
- A clear, high-level project description.
- List of technical constraints (e.g., Python 3.13+, Node 22+).

---

## 2. Requirements & Design (Spec)
**Goal:** Define *what* to build and *how* it should look/behave.

### Activities:
- **Requirement Definition**: List functional and non-functional requirements.
- **System Design**: Define the database schema, API endpoints, and directory structure.
- **UI/UX Design**: Draft UI layouts (e.g., List vs. Grid views, empty states) and user flows.
- **Document Creation**: Generate `0001-instructions.md`.

### Best Practice Prompts:
> **Security**: "Review the project configuration for security best practices, specifically regarding credential management and container permissions."
> **Frontend**: "Review the UI for user-friendliness and propose modern enhancements like card views and empty states."

### Output:
- `spec/weekXX/0001-instructions.md` containing:
  - Functional Requirements
  - Database Schema
  - API Design (RESTful)
  - UI Preview (ASCII/Wireframes)
  - Tech Stack & Versions

---

## 3. Implementation Planning (Plan)
**Goal:** Break down the work into actionable steps.

### Activities:
- **Task Breakdown**: Create a step-by-step checklist (Phase 1: Setup, Phase 2: Backend, Phase 3: Frontend, etc.).
- **Dependency Check**: Verify all required libraries and versions (pin dependencies).
- **Document Creation**: Generate `0001-implementation-plan.md`.

### Best Practice Prompts:
> **Infrastructure**: "Check and update dependency versions to the latest stable releases (e.g., PG 17+, Python 3.13+)."

### Output:
- `spec/weekXX/0001-implementation-plan.md` containing:
  - Checklist of tasks.
  - Verification steps for each phase.

---

## 4. Development (Code)
**Goal:** Write the code according to the plan.

### Activities:
- **Infrastructure Setup**: Configure Docker, gitignore, and linters.
- **Backend Dev**: Implement Models, Schemas, and API endpoints.
- **Frontend Dev**: Build Views, Components, and integrate API.
- **Iterative Coding**: Follow the plan item by item, updating the Todo list.

### Best Practice Prompts:
> **Security**: "Ensure no secrets are hardcoded. Use .env and pydantic-settings."

### Output:
- Source code in `./weekXX/` folder.
- Working local environment (Docker Compose).

---

## 5. Verification & Delivery (Test & Commit)
**Goal:** Ensure quality and finalize the work.

### Activities:
- **Unit Testing**: Write and run backend tests (`pytest`). Target >95% coverage.
- **CI/CD**: Setup GitHub Actions for automated testing.
- **Manual Review**: Verify UI responsiveness, empty states, and error handling.
- **Documentation**: Update README and API docs (Swagger/ReDoc).
- **Final Commit**: Generate a clean commit message and submit.

### Best Practice Prompts:
> **Testing**: "Setup a robust testing infrastructure targeting >95% code coverage, including edge cases and CI integration."
> **Documentation**: "Verify API documentation availability and update the project specs with deployment details."

### Output:
- Verified Codebase.
- CI/CD Workflow (`.github/workflows/ci.yml`).
- High Test Coverage Report.
- Final `README.md`.

---

## Example: Week01-TagTrack Workflow

### 1. Requirements (Spec)
User wants a ticket management tool.
- **Backend**: FastAPI, AsyncSQLAlchemy, Postgres.
- **Frontend**: Vue 3, Element Plus.
- **Features**: CRUD Tickets/Tags, Batch Delete, Filtering.

### 2. Plan
1.  **Setup**: Docker Compose, Git repo.
2.  **Backend**: DB Models, Migrations, API Endpoints.
3.  **Frontend**: Ticket View (List/Grid), Tag View.
4.  **Testing**: Pytest setup.

### 3. Execution
- Implemented `week1/backend` and `week1/frontend`.
- Added `pytest-cov` and achieved 98% coverage.
- Added GitHub Actions CI.
- Refined UI with Grid View and Empty States.

### 4. Review
- Verified all requirements met.
- Security checks passed (non-root user, no hardcoded secrets).
