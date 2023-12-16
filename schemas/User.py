from pydantic import BaseModel, ConfigDict, EmailStr
from typing import List, Optional

from schemas.Role import RoleCreate


class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserCreate(UserBase):
    rol: RoleCreate


class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[str]
    roles: Optional[List[RoleCreate]]


class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
