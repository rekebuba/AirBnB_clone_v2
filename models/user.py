#!/usr/bin/python3
"""User Class"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from models import storage_type
from sqlalchemy.orm import relationship

class User(BaseModel, Base):
    """Class for managing User objects"""
    __tablename__ ='users'
    if storage_type == 'db':
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128))
        last_name = Column(String(128))
        places = relationship('Place', backref='User', cascade="all, delete")
        reviews = relationship('Review', backref='user', cascade='all, delete')
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""
