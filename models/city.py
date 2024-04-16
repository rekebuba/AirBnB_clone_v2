#!/usr/bin/python3
"""City Class"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from models import storage_type

class City(BaseModel, Base):
    """Class for managing City objects"""
    __tablename__ = 'cities'
    if storage_type == 'db':
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('State.id'), nullable=False)
    else:
        state_id = ""
        name = ""
