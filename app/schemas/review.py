"""
Esquemas Pydantic para estructura y validación de datos de reseñas (reviews)
"""

from pydantic import BaseModel, ConfigDict, field_validator

# Modelo de respuesta (GET)
class ReviewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    videogame_id: int
    rating: float
    comment: str | None

# Modelo para crear reseñas (POST)
class ReviewCreate(BaseModel):
    user_id: int
    videogame_id: int
    rating: float
    comment: str | None = None

    @field_validator('rating')
    @classmethod
    def validate_rating(cls, v: float | str) -> float:
        # permitir que venga como "8,6" o "8.6"
        if isinstance(v, str):
            v = v.replace(',', '.')
        v = float(v)
        if not (1 <= v <= 10):
            raise ValueError('El rating debe estar entre 1 y 10')
        return round(v, 1)  # redondea a un decimal

# Modelo para actualizar reseñas (PUT)
# Todos los campos obligatorios
class ReviewUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    videogame_id: int
    rating: float
    comment: str | None = None

    @field_validator('rating')
    @classmethod
    def validate_rating(cls, v: float | str) -> float:
        if isinstance(v, str):
            v = v.replace(',', '.')
        v = float(v)
        if not (1 <= v <= 10):
            raise ValueError('El rating debe estar entre 1 y 10')
        return round(v, 1)

# Modelo para actualización parcial (PATCH)
# Solo se envían los campos a modificar
class ReviewPatch(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int | None = None
    videogame_id: int | None = None
    rating: float | None = None
    comment: str | None = None

    @field_validator('rating')
    @classmethod
    def validate_rating(cls, v: float | str | None) -> float | None:
        if v is None:
            return None
        if isinstance(v, str):
            v = v.replace(',', '.')
        v = float(v)
        if not (1 <= v <= 10):
            raise ValueError('El rating debe estar entre 1 y 10')
        return round(v, 1)
