#!/usr/bin/python3
from datetime import datetime
import uuid


class BaseModel:
    """
    defines all common attributes/methods for other classes
    """
    def __init__(self):
        """Public instance attributes"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """
        updates the public instance attribute updated_at with the current datetime
        """
        self.updated_at = datetime.now()
    
    def to_dict(self):
        """
        returns a dictionary containing all key/values of __dict__ of datetime
        """
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = self.__class__.__name__
        obj_dict['updated_at'] = self.updated_at.isoformat()
        obj_dict['created_at'] = self.created_at.isoformat()
        return obj_dict
    
    def __str__(self):
        """Return a string representation"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
