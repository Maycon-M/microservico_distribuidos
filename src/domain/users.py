from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    timezone: str = "America/Sao_Paulo"

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    timezone: str
    model_config = ConfigDict(from_attributes=True)
