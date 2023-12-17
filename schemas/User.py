from pydantic import BaseModel, ConfigDict, EmailStr
from typing import List, Optional

from schemas.Role import RoleCreate, Role


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
    is_active: bool
    roles: List[Role]

    model_config = ConfigDict(from_attributes=True)
