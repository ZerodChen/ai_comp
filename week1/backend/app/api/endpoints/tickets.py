import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import or_, delete, func

from app.db.session import get_db
from app.models.ticket import Ticket
from app.models.tag import Tag
from app.schemas.ticket import TicketCreate, TicketUpdate, Ticket as TicketSchema, TicketPage

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/", response_model=TicketSchema, status_code=status.HTTP_201_CREATED)
async def create_ticket(ticket: TicketCreate, db: AsyncSession = Depends(get_db)):
    logger.info(f"Creating ticket with title: {ticket.title}")
    new_ticket = Ticket(title=ticket.title, description=ticket.description)
    
    if ticket.tags:
        logger.info(f"Associating tags: {ticket.tags}")
        result = await db.execute(select(Tag).filter(Tag.id.in_(ticket.tags)))
        tags = result.scalars().all()
        new_ticket.tags = tags
        
    db.add(new_ticket)
    await db.commit()
    await db.refresh(new_ticket)
    # Reload to get tags
    result = await db.execute(select(Ticket).options(selectinload(Ticket.tags)).filter(Ticket.id == new_ticket.id))
    created_ticket = result.scalars().first()
    logger.info(f"Ticket created successfully: {created_ticket.id}")
    return created_ticket

@router.get("/", response_model=TicketPage)
async def read_tickets(
    page: int = 1,
    size: int = 10,
    tag_id: Optional[int] = None,
    q: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    logger.info(f"Fetching tickets page={page}, size={size}, tag_id={tag_id}, q={q}")
    skip = (page - 1) * size
    
    # Filters
    filters = []
    if tag_id:
        filters.append(Ticket.tags.any(Tag.id == tag_id))
    if q:
        filters.append(or_(Ticket.title.ilike(f"%{q}%"), Ticket.description.ilike(f"%{q}%")))
    
    # Count
    count_query = select(func.count()).select_from(Ticket)
    if filters:
        count_query = count_query.filter(*filters)
    total = (await db.execute(count_query)).scalar() or 0
    
    # Data
    query = select(Ticket).options(selectinload(Ticket.tags))
    if filters:
        query = query.filter(*filters)
        
    query = query.offset(skip).limit(size).order_by(Ticket.created_at.desc())
    
    result = await db.execute(query)
    items = result.scalars().all()
    logger.info(f"Found {len(items)} tickets (Total: {total})")
    return {"items": items, "total": total}

@router.get("/{ticket_id}", response_model=TicketSchema)
async def read_ticket(ticket_id: int, db: AsyncSession = Depends(get_db)):
    logger.info(f"Fetching ticket {ticket_id}")
    result = await db.execute(select(Ticket).options(selectinload(Ticket.tags)).filter(Ticket.id == ticket_id))
    ticket = result.scalars().first()
    if not ticket:
        logger.warning(f"Ticket {ticket_id} not found")
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@router.put("/{ticket_id}", response_model=TicketSchema)
async def update_ticket(ticket_id: int, ticket_update: TicketUpdate, db: AsyncSession = Depends(get_db)):
    logger.info(f"Updating ticket {ticket_id}")
    result = await db.execute(select(Ticket).options(selectinload(Ticket.tags)).filter(Ticket.id == ticket_id))
    ticket = result.scalars().first()
    if not ticket:
        logger.warning(f"Ticket {ticket_id} not found for update")
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    if ticket_update.title is not None:
        ticket.title = ticket_update.title
    if ticket_update.description is not None:
        ticket.description = ticket_update.description
        
    if ticket_update.tags is not None:
        logger.info(f"Updating tags for ticket {ticket_id}: {ticket_update.tags}")
        tag_result = await db.execute(select(Tag).filter(Tag.id.in_(ticket_update.tags)))
        new_tags = tag_result.scalars().all()
        ticket.tags = new_tags
        
    await db.commit()
    await db.refresh(ticket)
    logger.info(f"Ticket {ticket_id} updated successfully")
    return ticket

@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ticket(ticket_id: int, db: AsyncSession = Depends(get_db)):
    logger.info(f"Deleting ticket {ticket_id}")
    result = await db.execute(select(Ticket).filter(Ticket.id == ticket_id))
    ticket = result.scalars().first()
    if not ticket:
        logger.warning(f"Ticket {ticket_id} not found for deletion")
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    await db.delete(ticket)
    await db.commit()
    logger.info(f"Ticket {ticket_id} deleted successfully")

@router.delete("/batch", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tickets_batch(ids: List[int], db: AsyncSession = Depends(get_db)):
    logger.info(f"Batch deleting tickets: {ids}")
    await db.execute(delete(Ticket).where(Ticket.id.in_(ids)))
    await db.commit()
    logger.info(f"Batch delete successful")
