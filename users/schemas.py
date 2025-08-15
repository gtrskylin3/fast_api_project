from typing import Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, ConfigDict, EmailStr

class CreateUser(BaseModel):
    email: EmailStr
    username: Annotated[str, MinLen(3), MaxLen(20)]

class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)
    
    username: str
    password: bytes
    email: EmailStr | None = None
    active: bool = True