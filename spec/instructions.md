# Instruction
## Week01-TagTrack 
### Requirement and designs
This is a simple tool that use tag to classify and manage the tickets. It use python fastAPI as backend and Vue 3 + Element Plus + Vite as the frontend, database is the postgret, for now user management module is not involed. Major features as below:
- Ticket creation/modification/bulk deletion
- Tag creation/modification/batch deletion
- Listing tickets by tag
- Listing tickets by ticket title or description.

check above idea and and then help to generate detailed requirements and designs then output to ./spec/week01/0001-instructions.md

please also supplement below content in the 0001-instructions.md:
* unit test case.
* UI design preview
* Local environment setup instructions.
* Deployment instruction for local dev and productions

### Implementation plan
Please check ./spec/week01/0001-instructions.md then generate a detailed implementation plan then output to ./spec/week01/0001-implementation-plan.md

### Implementation
check spec/week01/0001-implementation-plan.md, then implement project as it mentioned , sourcec code will be put under ./week1 folder

### Reviewing
please check spec/week01/0001-implementation-plan.md then review the implementation under ./week1 folder, if any issue or mismatch found, please update the plan and implementation.

### Project Standards & Best Practices (Prompts for Future Use)
Use the following checklist and guidelines when starting a new project or reviewing an existing one to ensure high quality, security, and maintainability.

#### 1. Security & Configuration
**Prompt:** "Review the project configuration for security best practices, specifically regarding credential management and container permissions."

- **Credentials**:
  - NEVER hardcode secrets in `config.py`, `alembic.ini`, or `Dockerfile`.
  - Use `.env` files for local development and exclude them via `.gitignore`.
  - Use `pydantic-settings` to read environment variables with fallbacks only for non-sensitive defaults.
  - In `docker-compose.yml`, inject secrets via `${VAR_NAME}` syntax.
- **Docker Security**:
  - Do NOT run containers as `root`. Create a non-root user (e.g., `appuser`) in the Dockerfile and switch to it using `USER appuser`.
  - Ensure entrypoint scripts handle permission requirements for generated files (e.g., migrations) gracefully or pre-create directories with correct ownership.

#### 2. Testing & Quality Assurance
**Prompt:** "Setup a robust testing infrastructure targeting >95% code coverage, including edge cases and CI integration."

- **Backend Testing**:
  - Use `pytest` with `pytest-asyncio` and `httpx`.
  - Use `aiosqlite` for fast in-memory database testing (`sqlite+aiosqlite:///:memory:`).
  - Configure `pytest.ini` to standardize test paths and async modes.
  - Install `pytest-cov` and configure `.coveragerc` to track coverage (target > 95%).
  - **Critical Scenarios**: Test CRUD, Batch Operations, Idempotency, Filters, Pagination, and Error Handling (404, 422).
- **CI/CD**:
  - Create a GitHub Action (`.github/workflows/ci.yml`) to run tests automatically on Pull Requests and Pushes.
  - Ensure CI uses the exact same Docker environment or dependency versions as production.

#### 3. Frontend & UX Design
**Prompt:** "Review the UI for user-friendliness and propose modern enhancements like card views and empty states."

- **View Modes**:
  - Support both **List View** (Table) for density/management and **Grid View** (Cards) for visual browsing.
  - Include a toggle button to switch modes.
- **Empty States**:
  - Never show just a blank table. Use components like `el-empty` to display a friendly message when no data is found.
- **Interactivity**:
  - Use loading spinners (`v-loading`) during data fetches.
  - Use confirmation dialogs (`ElMessageBox`) for destructive actions (Delete).
  - Add toast notifications (`ElMessage`) for success/error feedback.

#### 4. Infrastructure & Versioning
**Prompt:** "Check and update dependency versions to the latest stable releases."

- **Stack Versions**:
  - Python: Use latest stable (e.g., `3.13+`).
  - Node.js: Use latest LTS (e.g., `22+`).
  - PostgreSQL: Use latest stable (e.g., `17+`).
- **Dependency Management**:
  - Pin versions in `requirements.txt` or `package.json` to avoid "it works on my machine" issues.
  - Use multi-stage Docker builds to keep images slim.

#### 5. Documentation
**Prompt:** "Verify API documentation availability and update the project specs with deployment details."

- **API Docs**:
  - Leverage FastAPI's auto-generated docs: Swagger UI (`/docs`) and ReDoc (`/redoc`).
  - Explicitly mention these URLs in the README/Instructions.
- **Setup Instructions**:
  - Provide clear steps for Local Dev (Docker Compose) vs. Production.
  - Document how to run tests locally (`docker-compose exec backend pytest`).

## Week2 - DbQueryHelper
### Porject Requirement and design
This tool is a helper to query database. It provides a simple interface for user to query provided database in natual languange or SQL.
Basic flow:
- **Connect & Index**: User provides a DB URL; the tool connects, caches metadata in SQLite, and displays available tables/views.
- **Natural Language Query**: Converts natural language questions into SQL using an LLM (online or local) and executes them.
- **SQL Query**: Validates raw SQL for syntax errors and security risks before execution.

Core features:
- Unified interface for querying multiple databases.
- Support for both natural language and raw SQL inputs.
- Multi-database connection support.
- Secure query validation and execution.
- Export query results to CSV or JSON.

Technical stack:
- **Backend**: FastAPI, SQLAlchemy, Alembic, Pydantic.
- **Frontend**: Vue.js, Element Plus.
- **Database**: SQLite (for metadata storage).
- **LLM Integration**: OpenAI API or local models (e.g., via `transformers`).
- **Deployment**: Docker Compose for local dev, Kubernetes for production.

As per above requirement, please help to design the project then generate the detailed requirements and designs to ../week2/spec/0001-instructions.md, don't forget below content:
* unit test case, coverage is over 90%.
* UI design preview, 2 UI mode could support switching.
* Local environment setup instructions.
* Deployment instruction for local dev and productions

### Implementation plan
please help to generate detailed implementation plan as per ../week2/spec/0001-instructions.md, I know that this tool is a bit complex, you could implement it in different no more than 4 phases, each phase should have clear deliverables and timelines. this implementaion plan will be output to ../week2/spec/0002-implementation-plan.md.

### Implementation
please check #0002-implementation-plan.md for detailed implementation plan then implementa phase1 as mentioned, sources code will be put under ../week2, please also help to add necessary comments and docstrings to the code and generate a readme under week2 directory.