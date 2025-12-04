"""
Router de páginas web
Contienen los endpoints que renderizan HTMLs
"""


from fastapi import APIRouter
from app.routers.web import genres
from app.routers.web import users
from app.routers.web import home


# main router
router = APIRouter()

# include genre and videogame router in the main router
router.include_router(genres.router)
router.include_router(users.router)
router.include_router(home.router)
