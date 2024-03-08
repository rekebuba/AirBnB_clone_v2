#!/usr/bin/python3
from models.base_model import BaseModel
from models import storage

class User(BaseModel):
    """a class User that inherits from BaseModel"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
    
