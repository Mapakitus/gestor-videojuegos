


from pydantic import BaseModel, ConfigDict, field_validator


class DevResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    image_url: str | None


class DevCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    image_url: str

    @field_validator("name", "image_url")
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("El campo nombre no puede estar vacío")
        
        return v.strip()
    
class DevUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    image_url: str

    @field_validator("name", "image_url")
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("El campo nombre no puede estar vacío")
        
        return v.strip()
    

class DevPatch(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str | None = None
    image_url: str | None = None

    @field_validator("name", "image_url")
    @classmethod
    def validate_not_empty(cls, v: str | None) -> str | None:
        if v is None:
            return None

        v = v.strip()

        if not v:
            raise ValueError("El campo nombre no puede estar vacío")
        
        return v