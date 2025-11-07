# modelo de juego de la aplicacion
from pydantic import BaseModel, Field
from typing import List, Optional

from models.domain.developer_model import DeveloperModel

class GameModel(BaseModel):
    id: str = Field(..., description="Identificador único del juego UUID",) # uuid
    title: str = Field(..., description="Título del juego")
    date_release: Optional[str] = Field(None, description="Fecha de lanzamiento del juego en formato YYYY-MM-DD")
    genres: List[str] = Field(default_factory=list, description="Lista de géneros del juego")
    platform: Optional[str] = Field(None, description="Plataforma del juego ( PC, PS5, Xbox, etc.)")
    developer: DeveloperModel = Field(..., description="Desarrollador del juego")