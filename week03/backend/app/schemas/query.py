from pydantic import BaseModel
from typing import List, Dict, Any, Union, Optional

class SQLQueryRequest(BaseModel):
    connection_id: int
    sql: str

class NLQueryRequest(BaseModel):
    connection_id: int
    question: str

class ExportQueryRequest(BaseModel):
    connection_id: int
    sql: str
    format: str

class QueryResponse(BaseModel):
    data: Optional[List[Dict[str, Any]]] = None
    sql: Optional[str] = None
    error: Optional[str] = None
    suggested_export_format: Optional[str] = None
