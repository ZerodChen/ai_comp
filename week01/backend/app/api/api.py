from fastapi import APIRouter
from app.api.endpoints import tickets, tags

api_router = APIRouter()
api_router.include_router(tickets.router, prefix="/tickets", tags=["tickets"])
api_router.include_router(tags.router, prefix="/tags", tags=["tags"])
