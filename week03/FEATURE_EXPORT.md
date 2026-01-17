# Feature: Data Export Functionality

## 1. Overview
Enhance the Database Query Tool to support exporting query results to CSV and JSON formats. This includes manual export via UI buttons and automated export capabilities based on user intent.

## 2. Design

### 2.1 Backend
- **New Service**: `ExportService` in `app/services/export_service.py`.
  - Responsibilities:
    - Execute SQL (re-using `QueryService` logic or helper).
    - Format data as CSV or JSON string/stream.
- **API Endpoint**: `POST /api/query/export`
  - Input: `connection_id`, `sql`, `format` (enum: 'csv', 'json').
  - Output: File stream (`StreamingResponse`) with appropriate headers (`Content-Disposition`).
- **LLM Enhancement**:
  - Update `LLMService` to detect "export intent" in natural language queries.
  - Return this intent to the frontend so it can auto-trigger the export or prompt the user.

### 2.2 Frontend
- **API Client**: Add `exportData` function to `src/api/query.js`.
- **UI Changes**:
  - Add "Export as CSV" and "Export as JSON" buttons in `QueryInterface.vue` (visible after results are loaded).
  - Implement a mechanism to handle the file download from the binary response.
- **Automated Workflow**:
  - If the NL query implies export (e.g., "Get users and save as csv"), the frontend receives this flag and automatically triggers the download or shows a confirmation toast.

### 2.3 User Interaction
- **Proactive Prompt**: After a query execution, if the result set is large or if the LLM detects a potential need, the UI can show a subtle prompt: "Would you like to download these results?"
- **Natural Language Trigger**: Users can type "Export to CSV" in the chat interface.

## 3. Implementation Steps
1.  **Backend**: Implement `ExportService` and API endpoint.
2.  **Backend**: Update `LLMService` to extract export format intent.
3.  **Frontend**: Add API method for export.
4.  **Frontend**: Add UI buttons and download handler.
5.  **Frontend**: Integrate "auto-export" logic based on LLM response.
