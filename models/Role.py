from sqlalchemy import Table, Column, Integer, JSON, ForeignKey, Enum as SqlAlchemyEnum
from sqlalchemy.orm import relationship
from enum import Enum

from config.db import Base


class RolName(str, Enum):
    MANAGER = "MANAGER"
    TEACHER = "TEACHER"
    STUDENT = "STUDENT"


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(SqlAlchemyEnum(RolName, create_constraint=True))
    permissions = Column(JSON)
    users = relationship('User', secondary='user_roles', back_populates='roles')


user_roles = Table('user_roles', Base.metadata,
                   Column('user_id', Integer, ForeignKey('users.id')),
                   Column('role_id', Integer, ForeignKey('roles.id')))
