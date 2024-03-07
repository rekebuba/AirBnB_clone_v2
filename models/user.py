#!/usr/bin/python3
from models.base_model import BaseModel
from models import storage

class User(BaseModel):
    """a class User that inherits from BaseModel"""
    def __init__(self):
        self.email = ""
        self.password = ""
        self.first_name = ""
        self.last_name = ""
        self.id = BaseModel().id
        
