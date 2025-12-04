from pydantic import BaseModel, ConfigDict, field_validator

# PYDANTIC MODELS (schemas)
# models that validate the data entering and leaving the API

# schema for ALL API responses
# used in GET, POST, PUT, PATCH

class GenreResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    image_url: str

# schema for CREATING a genre (POST)
class GenreCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: str
    image_url: str

    @field_validator("name", "description", "image_url")
    @classmethod
    def validate_title_not_empty(cls, v: str) -> str:
        # check if the value is empty or contains only spaces
        if not v or not v.strip():
            raise ValueError("Este campo no puede estar vacío")
        
        # returns the value without leading and trailing spaces
        return v.strip()
    
class GenreUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: str
    image_url: str

    @field_validator("name", "description", "image_url")
    @classmethod
    def validate_title_not_empty(cls, v: str) -> str:
        # check if the value is empty or contains only spaces
        if not v or not v.strip():
            raise ValueError("Este campo no puede estar vacío")
        
        # returns the value without leading and trailing spaces
        return v.strip()

class GenrePatch(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str | None = None
    description: str | None = None
    image_url: str | None = None

    @field_validator("name", "description", "image_url")
    @classmethod
    def validate_not_empty(cls, v: str | None) -> str | None:
        # if no value is provided (None), we skip validation
        if v is None:
            return None
        
        # if a value is provided, validate that it is not empty
        if not v or not v.strip():
            raise ValueError("Este campo no puede estar vacío")
        
        return v.strip()
    


    

