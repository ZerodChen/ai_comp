# Spec-Driven Development Playbook

This document acts as a "Prompt Book" to help you efficiently drive the AI to build new tools using the **Spec-Driven Development** methodology.

**How to use:**
1.  **Copy-paste** the content of each step into the chat with the AI.
2.  **Fill in** the placeholders (e.g., `<YOUR_IDEA_HERE>`) in Step 1.
3.  **Execute** the steps sequentially.

---

## Phase 1: Idea Definition & Spec Generation

**Goal:** Turn your raw idea into a detailed technical specification.

**Copy & Paste into Chat:**
```markdown
# Role: Architect & Tech Lead

# Context
I want to build a new tool/application. 
Here is the high-level idea:
<YOUR_IDEA_HERE>
(Example: "A simple ToDo app using FastAPI and Vue3. Features: Add task, list tasks, mark done. DB: SQLite.")

# Task
1. Analyze the idea above.
2. Generate a detailed requirements and design document.
3. Output the content to `./spec/<PROJECT_NAME>/0001-instructions.md`.

# Requirements for the Spec
Please include the following sections in the `0001-instructions.md`:
- **Project Overview**: High-level summary.
- **Tech Stack**: Backend, Frontend, Database, ORM, etc. (Prefer latest stable versions: Python 3.13+, Node 22+, PG 17+).
- **Functional Requirements**: Detailed feature list (CRUD, Filters, Batch Ops).
- **Database Design**: Schema, Tables, Relationships.
- **API Design**: RESTful endpoints, Methods, Payloads.
- **Frontend Design**: Layouts, Views (List/Grid), Components, Interactivity (Empty states, Loading).
- **Project Structure**: Proposed directory tree.
- **Testing Strategy**: Backend (pytest >95% coverage) & Frontend strategy.
- **Environment Setup**: Local Dev (Docker Compose) & Production Deployment steps.
```

---

## Phase 2: Implementation Planning

**Goal:** Create a step-by-step actionable plan for the AI to execute.

**Copy & Paste into Chat:**
```markdown
# Role: Technical Project Manager

# Context
The requirements are defined in `./spec/<PROJECT_NAME>/0001-instructions.md`.

# Task
1. Read and analyze the specification file.
2. Generate a detailed, step-by-step implementation plan.
3. Output the plan to `./spec/<PROJECT_NAME>/0001-implementation-plan.md`.

# Requirements for the Plan
- Break down the work into logical phases (e.g., Setup, Backend Core, API, Frontend Base, Frontend Features, Polish).
- Ensure each step is atomic and verifiable.
- Include a "Verification" step for each phase (e.g., "Run server and check health endpoint").
- **Crucial**: Include a phase for "Quality Assurance" that enforces:
  - Security checks (Non-root Docker users, No hardcoded secrets).
  - Test coverage (>95% backend coverage with edge cases).
```

---

## Phase 3: Execution (Coding)

**Goal:** Write the actual code based on the approved plan.

**Copy & Paste into Chat:**
```markdown
# Role: Senior Full-Stack Developer

# Context
The implementation plan is ready at `./spec/<PROJECT_NAME>/0001-implementation-plan.md`.

# Task
1. Read the implementation plan.
2. Execute the plan phase by phase.
3. Place the source code under the `./<PROJECT_NAME>` folder.

# Constraints & Standards
- **Security**: Use `.env` for secrets. Never hardcode credentials. Run Docker as non-root.
- **Testing**: Write tests *alongside* code. Do not wait for the end. Target >95% coverage.
- **Frontend**: Use `el-empty` for empty states, `v-loading` for async states, and support Grid/List toggles if applicable.
- **Verification**: After completing each major step, run the verification command (e.g., `pytest`, `npm run dev`) to ensure stability.
```

---

## Phase 4: Review & Refinement

**Goal:** Polish the result and ensure it meets high standards.

**Copy & Paste into Chat:**
```markdown
# Role: QA & Security Auditor

# Context
The implementation is complete under `./<PROJECT_NAME>`.

# Task
1. Review the codebase against the plan in `./spec/<PROJECT_NAME>/0001-implementation-plan.md`.
2. Perform a security review (Dockerfile user, Config secrets).
3. Perform a test coverage review (Run `pytest --cov`).
4. Perform a UI/UX review (Check for empty states, loading indicators).

# Action
If any issue or mismatch is found, fix it immediately.
If the coverage is below 95%, write additional tests (edge cases, batch ops).
If the UI lacks polish, add the missing user-friendly features.
```

---

## Appendix: Quality Standards Checklist
(Reference these when prompting for specific tasks)

**1. Security**:
- [ ] Non-root user in Dockerfile.
- [ ] Secrets in `.env` only.
- [ ] `pydantic-settings` for config.

**2. Testing**:
- [ ] `pytest-asyncio` + `httpx`.
- [ ] `aiosqlite` for in-memory DB tests.
- [ ] >95% Coverage.
- [ ] CI/CD Workflow (`.github/workflows/ci.yml`).

**3. UX**:
- [ ] Grid/List View Toggles.
- [ ] Empty States.
- [ ] Loading Spinners.
- [ ] Destructive Action Confirmations.
