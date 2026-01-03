from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.query import SQLQueryRequest, NLQueryRequest, QueryResponse
from app.services.query_service import QueryService
from app.services.llm_service import LLMService

router = APIRouter()

@router.post("/sql", response_model=QueryResponse)
def execute_sql(request: SQLQueryRequest, db: Session = Depends(get_db)):
    service = QueryService(db)
    try:
        data = service.execute_sql(request.connection_id, request.sql)
        if isinstance(data, dict):
             return QueryResponse(data=[data], sql=request.sql)
        return QueryResponse(data=data, sql=request.sql)
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/natural-language", response_model=QueryResponse)
def execute_nl_query(request: NLQueryRequest, db: Session = Depends(get_db)):
    llm_service = LLMService(db)
    query_service = QueryService(db)
    
    try:
        # 1. Generate SQL
        generated_sql = llm_service.generate_sql(request.connection_id, request.question)
        
        # 2. Execute SQL
        data = query_service.execute_sql(request.connection_id, generated_sql)
        
        if isinstance(data, dict):
             return QueryResponse(data=[data], sql=generated_sql)
             
        return QueryResponse(data=data, sql=generated_sql)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
