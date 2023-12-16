from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from config.db import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True)
    email = Column(String(150), unique=True)
    password = Column(String(150))
    roles = relationship('Role', secondary='user_roles', back_populates='users')
