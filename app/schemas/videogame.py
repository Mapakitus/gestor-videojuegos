"""
Esquemas Pydantic para estructura y validación de datos de videojuegos
"""

from pydantic import BaseModel, ConfigDict, field_validator


# Modelo de respuesta (GET)
class VideogameResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str | None
    genre_id: int
    developer_id: int


# Modelo para crear videojuegos (POST)
class VideogameCreate(BaseModel):
    title: str
    description: str | None = None
    genre_id: int
    developer_id: int

    @field_validator('title')
    @classmethod
    def validate_title_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('El título no puede estar vacío o contener solo espacios en blanco.')
        return v.strip()

    @field_validator('description')
    @classmethod
    def validate_description_not_empty(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError('La descripción no puede contener solo espacios en blanco.')
        return v.strip() if v is not None else None


# Modelo para actualizar videojuegos (PUT)
# Todos los campos son obligatorios
class VideogameUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    description: str | None
    genre_id: int
    developer_id: int

    @field_validator('title')
    @classmethod
    def validate_title_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('El título no puede estar vacío o contener solo espacios en blanco.')
        return v.strip()

    @field_validator('description')
    @classmethod
    def validate_description_not_empty(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError('La descripción no puede contener solo espacios en blanco.')
        return v.strip() if v is not None else None


# Modelo para actualización parcial (PATCH)
# Solo se envían los campos a modificar
class VideogamePatch(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str | None = None
    description: str | None = None
    genre_id: int | None = None
    developer_id: int | None = None

    @field_validator('title')
    @classmethod
    def validate_title_not_empty(cls, v: str | None) -> str | None:
        if v is None:
            return None
        if not v.strip():
            raise ValueError('El título no puede estar vacío o contener solo espacios en blanco.')
        return v.strip()

    @field_validator('description')
    @classmethod
    def validate_description_not_empty(cls, v: str | None) -> str | None:
        if v is None:
            return None
        if not v.strip():
            raise ValueError('La descripción no puede contener solo espacios en blanco.')
        return v.strip()
