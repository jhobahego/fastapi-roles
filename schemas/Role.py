from pydantic import BaseModel, ConfigDict
from typing import List
from enum import Enum


class Autority(str, Enum):
    READ = "READ"
    CREATE = "CREATE"
    MODIFY = "MODIFY"
    DELETE = "DELETE"
    CHANGE_CREDENTIALS = "CHANGE_CREDENTIALS"


class RolName(str, Enum):
    MANAGER = "MANAGER"
    TEACHER = "TEACHER"
    STUDENT = "STUDENT"


class RoleCreate(BaseModel):
    name: RolName


class Role(RoleCreate):
    id: int
    permissions: List[Autority]

    model_config = ConfigDict(from_attributes=True)
