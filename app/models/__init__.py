"""
Modelos de base de datos (SQLAlchemy)
"""

from app.models.genre import GenreORM
from app.models.videogame import Videogame
from app.models.user import UserORM

__all__ = ["GenreORM", "Videogame", "UserORM"]