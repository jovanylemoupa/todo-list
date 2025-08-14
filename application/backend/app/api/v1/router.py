from fastapi import APIRouter
from .endpoints import tasks, categories

# Router principal de l'API v1
api_router = APIRouter(prefix="/api/v1")

# Inclusion des routers d'endpoints
api_router.include_router(tasks.router)
api_router.include_router(categories.router)