#!/usr/bin/python3
"""User Class"""

from models.base_model import BaseModel
from sqlalchemy import Column, String
from models import storage_type
from sqlalchemy.orm import relationships

class User(BaseModel):
    """Class for managing User objects"""
    __tablename__ ='users'
    if storage_type == 'db':
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128))
        last_name = Column(String(128))
        places = relationships('place', backref='User', cascade="all, delete")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""
