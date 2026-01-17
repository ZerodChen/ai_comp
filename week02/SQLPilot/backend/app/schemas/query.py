from pydantic import BaseModel
from typing import List, Dict, Any, Union, Optional

class SQLQueryRequest(BaseModel):
    connection_id: int
    sql: str

class NLQueryRequest(BaseModel):
    connection_id: int
    question: str

class QueryResponse(BaseModel):
    data: Optional[List[Dict[str, Any]]] = None
    sql: Optional[str] = None
    error: Optional[str] = None
