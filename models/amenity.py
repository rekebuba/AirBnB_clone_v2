#!/usr/bin/python3
"""Amenity Class"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from models import storage_type


class Amenity(BaseModel, Base):
    """Class for managing amenity objects"""
    __tablename__ = 'amenities'
    if storage_type == 'db':
        name = Column(String(128), nullable=False)
    else:
        name = ""
