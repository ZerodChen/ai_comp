from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session
from app.models.metadata import DBConnection, TableMetadata, ColumnMetadata
import logging

logger = logging.getLogger(__name__)

class MetadataService:
    def __init__(self, db: Session):
        self.db = db

    def index_database(self, connection_id: int):
        connection = self.db.query(DBConnection).filter(DBConnection.id == connection_id).first()
        if not connection:
            logger.error(f"Connection {connection_id} not found")
            return

        try:
            # Connect to the target database
            target_engine = create_engine(connection.connection_url)
            inspector = inspect(target_engine)

            # Clear existing metadata for this connection
            self.db.query(TableMetadata).filter(TableMetadata.connection_id == connection_id).delete()
            
            table_names = inspector.get_table_names()
            
            for table_name in table_names:
                table_metadata = TableMetadata(
                    connection_id=connection_id,
                    table_name=table_name
                )
                self.db.add(table_metadata)
                self.db.flush() # flush to get ID

                columns = inspector.get_columns(table_name)
                pk_constraint = inspector.get_pk_constraint(table_name)
                pks = pk_constraint.get('constrained_columns', [])
                
                # FKs
                fks = inspector.get_foreign_keys(table_name)
                fk_columns = [col for fk in fks for col in fk['constrained_columns']]

                for col in columns:
                    column_metadata = ColumnMetadata(
                        table_id=table_metadata.id,
                        column_name=col['name'],
                        data_type=str(col['type']),
                        is_primary_key=col['name'] in pks,
                        is_foreign_key=col['name'] in fk_columns
                    )
                    self.db.add(column_metadata)

            self.db.commit()
            logger.info(f"Successfully indexed database {connection.name}")

        except Exception as e:
            logger.error(f"Error indexing database {connection.name}: {e}")
            self.db.rollback()
            raise e
