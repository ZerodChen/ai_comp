from pydantic import BaseModel, ConfigDict
from datetime import datetime

class DBConnectionBase(BaseModel):
    name: str
    db_type: str
    connection_url: str

class DBConnectionCreate(DBConnectionBase):
    pass

class DBConnection(DBConnectionBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
