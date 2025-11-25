from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic import field_validator

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nick: str
    email: EmailStr
    nif: str | None
    password: str


class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    nick: str
    nif: str | None = None
    password: str
    
    @field_validator("nick")
    @classmethod
    def validate_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("El nick no puede estar vacío")
        
        return v

    @field_validator("nif")
    @classmethod
    def validate_not_empty(cls, v: str | None) -> str | None:
        if v is None:
            return None
        
        v = v.strip()
        return v or None
    
    @field_validator("password")
    @classmethod
    def validate_string_empty(cls, v: str) -> str:
        if len(v) < 8:
            return ValueError("La contraseña tiene que tener mínimo 8 carácteres")
        
        if " " in v:
            return ValueError("La contraseña no puede contener espacios")
        
        return v
    
class UserUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    nick: str
    nif: str | None
    password: str

    @field_validator( "nif")
    @classmethod
    def validate_not_empty(cls, v: str | None) -> str | None:
        if v is None:
            return None
        
        if not v or not v.strip():
            raise ValueError("Este campo no puede estar vacío")
        
        return v.strip()

class UserPatch(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr | None = None
    nick: str | None = None
    nif: str | None = None
    password: str | None = None

    @field_validator("nif", "nick", "password")
    @classmethod
    def validate_not_empty(cls, v: str | None) -> str | None:
        if v is None:
            return None
        
        v = v.strip()

        return v or None