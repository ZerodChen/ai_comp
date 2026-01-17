import pytest
from unittest.mock import MagicMock, patch
from app.services.export_service import ExportService
from app.schemas.query import ExportQueryRequest

# Sample data
SAMPLE_DATA = [
    {"id": 1, "name": "Alice", "role": "admin"},
    {"id": 2, "name": "Bob", "role": "user"}
]

def test_export_csv_formatting(db):
    service = ExportService(db)
    # Mock query service to avoid DB calls
    service.query_service = MagicMock()
    service.query_service.execute_sql.return_value = SAMPLE_DATA
    
    generator = service.export_data(1, "SELECT * FROM users", "csv")
    content = "".join(list(generator))
    
    # Check CSV format
    expected_header = "id,name,role"
    assert expected_header in content
    assert "1,Alice,admin" in content
    assert "2,Bob,user" in content

def test_export_json_formatting(db):
    service = ExportService(db)
    service.query_service = MagicMock()
    service.query_service.execute_sql.return_value = SAMPLE_DATA
    
    generator = service.export_data(1, "SELECT * FROM users", "json")
    content = "".join(list(generator))
    
    # Check JSON format
    assert '"name": "Alice"' in content
    assert '"role": "user"' in content
    # The JSON output is pretty-printed, so we check for structural elements flexibly
    assert '[' in content
    assert '{' in content
    assert '"id": 1' in content

def test_export_api_csv(client, db):
    # Patch the ExportService.export_data method to return a generator
    with patch("app.api.endpoints.query.ExportService") as MockService:
        mock_instance = MockService.return_value
        
        def mock_generator(*args, **kwargs):
            yield "id,name\n1,Test"
            
        mock_instance.export_data.side_effect = mock_generator
        
        response = client.post(
            "/api/v1/query/export",
            json={"connection_id": 1, "sql": "SELECT *", "format": "csv"}
        )
        
        assert response.status_code == 200
        # Check content type (allow charset)
        assert "text/csv" in response.headers["content-type"]
        assert "attachment; filename=export.csv" in response.headers["content-disposition"]
        assert response.text == "id,name\n1,Test"

def test_export_api_json(client, db):
    with patch("app.api.endpoints.query.ExportService") as MockService:
        mock_instance = MockService.return_value
        
        def mock_generator(*args, **kwargs):
            yield '[{"id": 1}]'
            
        mock_instance.export_data.side_effect = mock_generator
        
        response = client.post(
            "/api/v1/query/export",
            json={"connection_id": 1, "sql": "SELECT *", "format": "json"}
        )
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
        assert "attachment; filename=export.json" in response.headers["content-disposition"]
        assert response.text == '[{"id": 1}]'
