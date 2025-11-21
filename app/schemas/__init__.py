"""
Esquemas Pydantic para validación de datos
"""

from app.schemas.videogame import (
    VideogameResponse,
    VideogameCreate,
    VideogameUpdate,
    VideogamePatch
)

__all__ = ["VideogameResponse", "VideogameCreate", "VideogameUpdate", "VideogamePatch"]