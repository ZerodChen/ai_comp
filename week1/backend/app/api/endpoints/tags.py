import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.models.tag import Tag
from app.schemas.tag import TagCreate, Tag as TagSchema

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/", response_model=TagSchema, status_code=status.HTTP_201_CREATED)
async def create_tag(tag: TagCreate, db: AsyncSession = Depends(get_db)):
    logger.info(f"Creating tag: {tag.name}")
    result = await db.execute(select(Tag).filter(Tag.name == tag.name))
    if result.scalars().first():
        logger.warning(f"Tag creation failed: '{tag.name}' already exists")
        raise HTTPException(status_code=400, detail="Tag with this name already exists")
    
    new_tag = Tag(name=tag.name)
    db.add(new_tag)
    await db.commit()
    await db.refresh(new_tag)
    logger.info(f"Tag created successfully: {new_tag.id}")
    return new_tag

@router.get("/", response_model=List[TagSchema])
async def read_tags(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    logger.info(f"Fetching tags skip={skip}, limit={limit}")
    result = await db.execute(select(Tag).offset(skip).limit(limit))
    tags = result.scalars().all()
    logger.info(f"Found {len(tags)} tags")
    return tags

@router.put("/{tag_id}", response_model=TagSchema)
async def update_tag(tag_id: int, tag_update: TagCreate, db: AsyncSession = Depends(get_db)):
    logger.info(f"Updating tag {tag_id} to '{tag_update.name}'")
    result = await db.execute(select(Tag).filter(Tag.id == tag_id))
    tag = result.scalars().first()
    if not tag:
        logger.warning(f"Tag {tag_id} not found for update")
        raise HTTPException(status_code=404, detail="Tag not found")
    
    # Check name uniqueness if changed
    if tag.name != tag_update.name:
        existing = await db.execute(select(Tag).filter(Tag.name == tag_update.name))
        if existing.scalars().first():
            logger.warning(f"Tag update failed: name '{tag_update.name}' already taken")
            raise HTTPException(status_code=400, detail="Tag with this name already exists")
        tag.name = tag_update.name
        
    await db.commit()
    await db.refresh(tag)
    logger.info(f"Tag {tag_id} updated successfully")
    return tag

@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(tag_id: int, db: AsyncSession = Depends(get_db)):
    logger.info(f"Deleting tag {tag_id}")
    result = await db.execute(select(Tag).filter(Tag.id == tag_id))
    tag = result.scalars().first()
    if not tag:
        logger.warning(f"Tag {tag_id} not found for deletion")
        raise HTTPException(status_code=404, detail="Tag not found")
    
    await db.delete(tag)
    await db.commit()
    logger.info(f"Tag {tag_id} deleted successfully")

@router.delete("/batch", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tags_batch(ids: List[int], db: AsyncSession = Depends(get_db)):
    logger.info(f"Batch deleting tags: {ids}")
    # Using delete statement would be more efficient but keeping it simple with ORM for now or individual deletes
    # For bulk delete with SQLAlchemy async:
    from sqlalchemy import delete
    await db.execute(delete(Tag).where(Tag.id.in_(ids)))
    await db.commit()
    logger.info(f"Batch delete successful")
