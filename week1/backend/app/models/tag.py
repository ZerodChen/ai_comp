from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Tag(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    
    # Relationship
    tickets = relationship("Ticket", secondary="ticket_tags", back_populates="tags")
