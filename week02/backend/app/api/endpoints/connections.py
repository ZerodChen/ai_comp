from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db, SessionLocal
from app.models.metadata import DBConnection, TableMetadata
from app.schemas.connection import DBConnectionCreate, DBConnection as DBConnectionSchema
from app.services.metadata_service import MetadataService
from app.schemas.metadata import TableMetadata as TableMetadataSchema

router = APIRouter()

def index_db_task(connection_id: int):
    db = SessionLocal()
    try:
        service = MetadataService(db)
        service.index_database(connection_id)
    finally:
        db.close()

@router.post("/", response_model=DBConnectionSchema)
def create_connection(
    connection: DBConnectionCreate, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    db_connection = DBConnection(**connection.model_dump())
    db.add(db_connection)
    db.commit()
    db.refresh(db_connection)
    
    background_tasks.add_task(index_db_task, db_connection.id)
    return db_connection

@router.get("/", response_model=List[DBConnectionSchema])
def list_connections(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    connections = db.query(DBConnection).offset(skip).limit(limit).all()
    return connections

@router.get("/{connection_id}", response_model=DBConnectionSchema)
def get_connection(connection_id: int, db: Session = Depends(get_db)):
    connection = db.query(DBConnection).filter(DBConnection.id == connection_id).first()
    if connection is None:
        raise HTTPException(status_code=404, detail="Connection not found")
    return connection

@router.get("/{connection_id}/schema", response_model=List[TableMetadataSchema])
def get_connection_schema(connection_id: int, db: Session = Depends(get_db)):
    tables = db.query(TableMetadata).filter(TableMetadata.connection_id == connection_id).all()
    if not tables:
        # Check if connection exists to distinguish between "no tables" and "invalid connection"
        conn = db.query(DBConnection).filter(DBConnection.id == connection_id).first()
        if not conn:
            raise HTTPException(status_code=404, detail="Connection not found")
    return tables
