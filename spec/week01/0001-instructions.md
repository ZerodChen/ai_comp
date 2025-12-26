# Ticket Management Tool - Requirements and Design

## 1. Project Overview
This project is a simple ticket management tool that allows users to create, organize, and manage tickets using tags. It serves as a foundation for a task tracking system.

## 2. Tech Stack
- **Backend**: Python FastAPI
- **Frontend**: Vue 3 + Element Plus + Vite
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy (Async) / Pydantic for validation

## 3. Functional Requirements

### 3.1 Ticket Management
- **Create Ticket**: Users can create a new ticket with a title, description, and associate it with existing tags.
- **Modify Ticket**: Users can update the title, description, and tags of a ticket.
- **Delete Ticket**: Users can delete a single ticket.
- **Bulk Delete Tickets**: Users can select multiple tickets and delete them in one action.
- **List Tickets**:
    - Display a list of tickets.
    - Support pagination.
    - Filter by Tag.
    - Search by Ticket Title or Description.

### 3.2 Tag Management
- **Create Tag**: Users can create a new tag with a unique name.
- **Modify Tag**: Users can rename an existing tag.
- **Delete Tag**: Users can delete a tag.
- **Batch Delete Tags**: Users can delete multiple tags at once.
- **List Tags**: Display all available tags.

## 4. Database Design

### 4.1 Schema Overview
The database will consist of three main tables: `tickets`, `tags`, and an association table `ticket_tags` for the many-to-many relationship.

### 4.2 Tables

#### `tickets`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | PK, Auto-increment | Unique identifier |
| `title` | String(255) | Not Null | Ticket title |
| `description` | Text | Nullable | Detailed description |
| `created_at` | DateTime | Default: Now | Creation timestamp |
| `updated_at` | DateTime | Default: Now, OnUpdate: Now | Last update timestamp |

#### `tags`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | PK, Auto-increment | Unique identifier |
| `name` | String(50) | Not Null, Unique | Tag name |

#### `ticket_tags` (Association Table)
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `ticket_id` | Integer | FK -> tickets.id | |
| `tag_id` | Integer | FK -> tags.id | |
| | | PK(ticket_id, tag_id) | Composite Primary Key |

## 5. API Design (RESTful)

### 5.1 Tickets
- `POST /api/tickets/`: Create a new ticket.
- `GET /api/tickets/`: List tickets with query parameters:
    - `page`: Page number (default 1)
    - `size`: Items per page (default 10)
    - `tag_id`: Filter by tag ID (optional)
    - `q`: Search keyword for title/description (optional)
- `GET /api/tickets/{id}`: Get ticket details.
- `PUT /api/tickets/{id}`: Update ticket details.
- `DELETE /api/tickets/{id}`: Delete a single ticket.
- `DELETE /api/tickets/batch`: Bulk delete tickets (Body: `ids: List[int]`).

### 5.2 Tags
- `POST /api/tags/`: Create a new tag.
- `GET /api/tags/`: List all tags.
- `PUT /api/tags/{id}`: Update a tag.
- `DELETE /api/tags/{id}`: Delete a single tag.
- `DELETE /api/tags/batch`: Batch delete tags (Body: `ids: List[int]`).

## 6. Frontend Design

### 6.1 Layout
- **Main Layout**: A simple layout with a header (Title) and a main content area.
- **Navigation**: Tabs or a Sidebar to switch between "Tickets" and "Tags" views.

### 6.2 Views/Components

#### Ticket Management View
- **Search Bar**: Input for searching tickets by title/description.
- **Tag Filter**: Dropdown to filter tickets by specific tags.
- **Action Bar**: "New Ticket" button, "Delete Selected" button (disabled if no selection).
- **Ticket Table**:
    - Columns: Title, Description (truncated), Tags (badges), Created At, Actions (Edit/Delete).
    - Selection checkboxes for bulk actions.
    - Pagination controls at the bottom.
- **Ticket Dialog (Modal)**:
    - Form for Create/Edit.
    - Inputs: Title (Text), Description (Textarea), Tags (Multi-select dropdown).

#### Tag Management View
- **Action Bar**: "New Tag" button, "Delete Selected" button.
- **Tag Table**:
    - Columns: ID, Name, Actions (Edit/Delete).
    - Selection checkboxes.
- **Tag Dialog (Modal)**:
    - Form for Create/Edit.
    - Inputs: Name (Text).

## 7. Project Structure (Proposed)

```
project_root/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── endpoints/
│   │   │   │   ├── tickets.py
│   │   │   │   └── tags.py
│   │   │   └── api.py
│   │   ├── core/
│   │   │   └── config.py
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   └── session.py
│   │   ├── models/
│   │   │   ├── ticket.py
│   │   │   └── tag.py
│   │   ├── schemas/
│   │   │   ├── ticket.py
│   │   │   └── tag.py
│   │   └── main.py
│   ├── alembic/       # DB Migrations
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/       # API client calls
│   │   ├── components/
│   │   ├── views/
│   │   │   ├── TicketView.vue
│   │   │   └── TagView.vue
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   └── vite.config.js
└── spec/
    └── week01/
        └── 0001-instructions.md
```

## 8. Unit Testing Strategy

We will use `pytest` for backend testing and `Vitest` for frontend testing (optional but recommended).

### 8.1 Backend Test Cases
Tests should cover the following scenarios:

#### Ticket Module
- **`test_create_ticket`**: Verify ticket is created with correct title, description, and tags.
- **`test_create_ticket_invalid`**: Verify validation error for missing title.
- **`test_read_tickets`**: Verify pagination and correct return format.
- **`test_read_tickets_filter`**: Verify filtering by tag and search query works.
- **`test_update_ticket`**: Verify updating title and tags.
- **`test_delete_ticket`**: Verify ticket is removed from DB.
- **`test_bulk_delete_tickets`**: Verify multiple tickets are deleted.

#### Tag Module
- **`test_create_tag`**: Verify tag creation.
- **`test_create_duplicate_tag`**: Verify error when creating a tag with an existing name.
- **`test_update_tag`**: Verify tag renaming.
- **`test_delete_tag`**: Verify tag deletion and handling of associated tickets (should remove association, not ticket).

## 9. UI Design Preview

### 9.1 Ticket List View

```
+-----------------------------------------------------------------------+
|  Ticket Management Tool                               [Tags View >]   |
+-----------------------------------------------------------------------+
|  [ Search Tickets... ]  [ Filter by Tag v ]     [+ New Ticket]        |
|                                                 [ Delete Selected ]   |
+-----------------------------------------------------------------------+
|  [ ] | Title          | Tags       | Created At   | Actions           |
|  [x] | Fix Login Bug  | [Bug]      | 2023-10-25   | [Edit] [Delete]   |
|  [ ] | Add Dark Mode  | [Feature]  | 2023-10-26   | [Edit] [Delete]   |
|  [ ] | Update Docs    | [Docs]     | 2023-10-27   | [Edit] [Delete]   |
+-----------------------------------------------------------------------+
|  <  Prev  1  2  3  Next  >                                            |
+-----------------------------------------------------------------------+
```

### 9.2 Create/Edit Ticket Modal

```
+-------------------------------------------+
|  Create New Ticket                    [X] |
+-------------------------------------------+
|  Title:                                   |
|  [______________________________________] |
|                                           |
|  Description:                             |
|  [______________________________________] |
|  [______________________________________] |
|  [______________________________________] |
|                                           |
|  Tags:                                    |
|  [ Select Tags v ]                        |
|  (x) Bug  (x) High Priority               |
|                                           |
|                  [ Cancel ]  [ Save ]     |
+-------------------------------------------+
```

## 10. Local Environment Setup

### 10.1 Prerequisites
- Python 3.13+
- Node.js 22+
- PostgreSQL 17+

### 10.2 Backend Setup
1. **Navigate to backend**: `cd backend`
2. **Create virtual environment**: `python -m venv venv`
3. **Activate venv**:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. **Install dependencies**: `pip install -r requirements.txt`
5. **Configure Database**: Update `core/config.py` or set `.env` with DB credentials.
6. **Run Migrations**: The backend now includes an entrypoint script that automatically runs migrations on startup.
   - Manual (if needed): `alembic upgrade head`
7. **Start Server**: `uvicorn app.main:app --reload`

### 10.3 Frontend Setup
1. **Navigate to frontend**: `cd frontend`
2. **Install dependencies**: `npm install`
3. **Start Dev Server**: `npm run dev`

## 11. Deployment Instructions

### 11.1 Local Development (Docker Compose)
Create a `docker-compose.yml` in the root:

```yaml
version: '3.8'
services:
  db:
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: ticket_db
  backend:
    build: ./backend
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    volumes:
      - ./frontend:/app
```

Run `docker-compose up --build` to start the entire stack.

### 11.2 Production Deployment
1. **Database**: Use a managed PostgreSQL service (e.g., AWS RDS).
2. **Backend**:
   - Build a Docker image or use a process manager like Supervisor/Systemd.
   - Run with Gunicorn + Uvicorn workers: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app`
   - Set environment variables for production DB and secrets.
3. **Frontend**:
   - Build static assets: `npm run build`
   - Serve the `dist/` folder using Nginx or a CDN (e.g., Vercel, Netlify, AWS S3+CloudFront).
4. **Nginx Config (Example)**:
   ```nginx
   server {
       listen 80;
       server_name example.com;

       location / {
           root /var/www/frontend/dist;
           try_files $uri $uri/ /index.html;
       }

       location /api {
           proxy_pass http://localhost:8000;
       }
   }
   ```
