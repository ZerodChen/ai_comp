from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from app.models.metadata import DBConnection
from app.services.security_service import SecurityService
import logging

logger = logging.getLogger(__name__)

class QueryService:
    def __init__(self, db: Session):
        self.db = db
        self.security_service = SecurityService()

    def execute_sql(self, connection_id: int, sql: str):
        connection = self.db.query(DBConnection).filter(DBConnection.id == connection_id).first()
        if not connection:
            raise ValueError(f"Connection {connection_id} not found")

        # Validate SQL
        self.security_service.validate_sql(sql)

        try:
            # Create engine for the target database
            target_engine = create_engine(connection.connection_url)
            
            with target_engine.connect() as conn:
                result = conn.execute(text(sql))
                
                if result.returns_rows:
                    data = [dict(row) for row in result.mappings()]
                    return data
                else:
                    conn.commit()
                    return {"message": "Query executed successfully", "rows_affected": result.rowcount}

        except Exception as e:
            logger.error(f"Error executing query: {e}")
            raise e
