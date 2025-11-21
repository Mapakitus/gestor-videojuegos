"""
Esquemas Pydantic para validación de datos
"""

from app.schemas.videogame import (
    VideogameResponse,
    VideogameCreate,
    VideogameUpdate,
    VideogamePatch
)

from app.schemas.genre import (
    GenreResponse,
    GenreCreate,
    GenreUpdate,
    GenrePatch
)

__all__ = ["VideogameResponse", "VideogameCreate", "VideogameUpdate", "VideogamePatch", "GenreResponse", "GenreCreate", "GenreUpdate", "GenrePatch"]