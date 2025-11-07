from pydantic import BaseModel, Field
from typing import List, Optional

class DeveloperModel(BaseModel):
    id: str = Field(..., description="Identificador único del desarrollador UUID",) # uuid
    name: str = Field(..., description="Nombre del desarrollador")
    founded_date: Optional[str] = Field(None, description="Fecha de fundación del desarrollador en formato YYYY-MM-DD")
    country: Optional[str] = Field(None, description="País de origen del desarrollador")
