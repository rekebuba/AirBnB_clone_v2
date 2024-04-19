#!/usr/bin/python3
"""Review Class"""

from models.base_model import BaseModel, Base
from models import storage_type
from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, Base):
    """Class for managing Review objects"""
    __tablename__ = 'reviews'
    if storage_type == 'db':
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        text = Column(String(1024), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    else:
        place_id = ""
        text = ""
        user_id = ""
