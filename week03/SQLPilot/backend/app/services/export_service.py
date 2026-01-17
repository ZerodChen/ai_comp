import csv
import json
import io
from typing import List, Dict, Any, Generator
from sqlalchemy.orm import Session
from app.services.query_service import QueryService

class ExportService:
    def __init__(self, db: Session):
        self.query_service = QueryService(db)

    def export_data(self, connection_id: int, sql: str, format: str) -> Generator[str, None, None]:
        # Execute query using existing service logic
        # We need to get the raw result or data list. 
        # QueryService.execute_sql returns a list of dicts or a message dict.
        
        data = self.query_service.execute_sql(connection_id, sql)
        
        if isinstance(data, dict) and "message" in data:
            # It was a non-returning query (INSERT/UPDATE), nothing to export
            yield ""
            return

        if not data:
            yield ""
            return

        if format.lower() == 'csv':
            yield from self._to_csv(data)
        elif format.lower() == 'json':
            yield self._to_json(data)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def _to_csv(self, data: List[Dict[str, Any]]) -> Generator[str, None, None]:
        if not data:
            return
        
        output = io.StringIO()
        # Get headers from the first dictionary
        headers = list(data[0].keys())
        writer = csv.DictWriter(output, fieldnames=headers)
        
        # Write header
        writer.writeheader()
        yield output.getvalue()
        output.seek(0)
        output.truncate(0)
        
        # Write rows
        for row in data:
            writer.writerow(row)
            yield output.getvalue()
            output.seek(0)
            output.truncate(0)

    def _to_json(self, data: List[Dict[str, Any]]) -> str:
        # For JSON, we typically return the whole list at once or stream array elements.
        # Streaming valid JSON array is a bit tricky (comma handling), 
        # but for simplicity we can dump the whole thing if it fits in memory, 
        # or do a simple manual stream: [ ... , ... ]
        
        return json.dumps(data, default=str, indent=2)
