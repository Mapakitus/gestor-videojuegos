"""
Routers de API REST
Contiene los endpoints que devuelven datos en JSON
"""

from fastapi import APIRouter
from app.routers.api import genres

# main router
router = APIRouter()

# include genre router in the main router
router.include_router(genres.router)