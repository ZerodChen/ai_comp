from fastapi import APIRouter
from app.api.endpoints import connections, query

api_router = APIRouter()
api_router.include_router(connections.router, prefix="/connections", tags=["connections"])
api_router.include_router(query.router, prefix="/query", tags=["query"])
