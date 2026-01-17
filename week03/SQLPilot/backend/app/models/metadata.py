from typing import List, Optional
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class DBConnection(Base):
    __tablename__ = "db_connections"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    db_type: Mapped[str] = mapped_column(String(50)) # postgres, mysql, sqlite
    connection_url: Mapped[str] = mapped_column(String(500)) # Encrypted ideally
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    tables: Mapped[List["TableMetadata"]] = relationship(back_populates="connection", cascade="all, delete-orphan")

class TableMetadata(Base):
    __tablename__ = "table_metadata"

    id: Mapped[int] = mapped_column(primary_key=True)
    connection_id: Mapped[int] = mapped_column(ForeignKey("db_connections.id"))
    table_name: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    connection: Mapped["DBConnection"] = relationship(back_populates="tables")
    columns: Mapped[List["ColumnMetadata"]] = relationship(back_populates="table", cascade="all, delete-orphan")

class ColumnMetadata(Base):
    __tablename__ = "column_metadata"

    id: Mapped[int] = mapped_column(primary_key=True)
    table_id: Mapped[int] = mapped_column(ForeignKey("table_metadata.id"))
    column_name: Mapped[str] = mapped_column(String(100))
    data_type: Mapped[str] = mapped_column(String(50))
    is_primary_key: Mapped[bool] = mapped_column(Boolean, default=False)
    is_foreign_key: Mapped[bool] = mapped_column(Boolean, default=False)

    table: Mapped["TableMetadata"] = relationship(back_populates="columns")
