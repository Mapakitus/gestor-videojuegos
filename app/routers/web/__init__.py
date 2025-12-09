"""
Router de páginas web
Contienen los endpoints que renderizan HTMLs
"""


from fastapi import APIRouter
from app.routers.web import genres
from app.routers.web import users
from app.routers.web import home
from app.routers.web import videogame
from app.routers.web import developers
from app.routers.web import admin

# main router
router = APIRouter()


router.include_router(genres.router)
router.include_router(users.router)
router.include_router(home.router)
router.include_router(videogame.router)
router.include_router(developers.router)
router.include_router(admin.router)