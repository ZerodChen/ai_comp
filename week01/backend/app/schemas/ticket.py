from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from .tag import Tag

class TicketBase(BaseModel):
    title: str
    description: Optional[str] = None

class TicketCreate(TicketBase):
    tags: Optional[List[int]] = []

class TicketUpdate(TicketBase):
    title: Optional[str] = None
    tags: Optional[List[int]] = None

class Ticket(TicketBase):
    id: int
    created_at: datetime
    updated_at: datetime
    tags: List[Tag] = []

    class Config:
        from_attributes = True

class TicketPage(BaseModel):
    items: List[Ticket]
    total: int
