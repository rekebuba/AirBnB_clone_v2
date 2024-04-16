#!/usr/bin/python3
"""State Class"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models import storage_type

class State(BaseModel, Base):
    """Class for managing State objects"""
    __tablename__ = 'states'
    if storage_type == 'db':
        name = Column(String(128), nullable=False)
    else:
        name = ""
