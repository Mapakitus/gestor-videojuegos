"""
Routers de API REST
Contiene los endpoints que devuelven datos en JSON
"""

from fastapi import APIRouter
from app.routers.api import genres
from app.routers.api import videogames
from app.routers.api import users
from app.routers.api import developers


# main router
router = APIRouter()

# include genre and videogame router in the main router
router.include_router(genres.router)
router.include_router(videogames.router)
router.include_router(users.router)
router.include_router(developers.router)