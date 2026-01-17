from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.query import SQLQueryRequest, NLQueryRequest, QueryResponse, ExportQueryRequest
from app.services.query_service import QueryService
from app.services.llm_service import LLMService
from app.services.export_service import ExportService

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
        generated_sql, export_format = llm_service.generate_sql(request.connection_id, request.question)
        
        # 2. Execute SQL
        data = query_service.execute_sql(request.connection_id, generated_sql)
        
        if isinstance(data, dict):
             return QueryResponse(data=[data], sql=generated_sql, suggested_export_format=export_format)
             
        return QueryResponse(data=data, sql=generated_sql, suggested_export_format=export_format)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/export")
def export_query_result(request: ExportQueryRequest, db: Session = Depends(get_db)):
    service = ExportService(db)
    try:
        # Use generator to stream response
        stream = service.export_data(request.connection_id, request.sql, request.format)
        
        filename = f"export.{request.format}"
        media_type = "text/csv" if request.format == "csv" else "application/json"
        
        return StreamingResponse(
            stream, 
            media_type=media_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
