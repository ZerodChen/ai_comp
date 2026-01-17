from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class ColumnMetadata(BaseModel):
    column_name: str
    data_type: str
    is_primary_key: bool
    is_foreign_key: bool
    model_config = ConfigDict(from_attributes=True)

class TableMetadata(BaseModel):
    table_name: str
    description: Optional[str] = None
    columns: List[ColumnMetadata]
    model_config = ConfigDict(from_attributes=True)
