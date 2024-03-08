#!/usr/bin/python3
"""User Class"""
from models.base_model import BaseModel


class User(BaseModel):
    """Class for managing User objects"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
