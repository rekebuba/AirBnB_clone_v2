#!/usr/bin/python3
"""Module for Base_model"""
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from datetime import datetime
import uuid
from models import storage_type


Base = declarative_base()


class BaseModel:
    """defines all common attributes/methods for other classes"""
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow(), nullable=False)

    def __init__(self, *args, **kwargs):
        """Public instance attributes"""
        if kwargs is not None and kwargs != {}:
            for key, value in kwargs.items():
                if key in ['created_at', 'updated_at']:
                    setattr(self, key, datetime.fromisoformat(value))
                elif key != '__class__':
                    setattr(self, key, value)
            if storage_type == 'db':
                if not hasattr(kwargs, 'id'):
                    setattr(self, 'id', str(uuid.uuid4()))
                if not hasattr(kwargs, 'created_at'):
                    setattr(self, 'created_at', datetime.now())
                if not hasattr(kwargs, 'updated_at'):
                    setattr(self, 'updated_at', datetime.now())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def save(self):
        """updates the public instance attribute updated_at
        with the current datetime"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """
        returns a dictionary containing all key/values of __dict__ of datetime
        """
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = self.__class__.__name__
        for k in obj_dict:
            if type(obj_dict[k]) is datetime:
                obj_dict[k] = obj_dict[k].isoformat()
        if '_sa_instance_state' in obj_dict.keys():
            del(obj_dict['_sa_instance_state'])
        return obj_dict
        return obj_dict

    def delete(self):
        from models import storage
        storage.delete(self)

    def __str__(self):
        """Return a string representation"""
        return f"[{type(self).__name__}] ({self.id}) {self.__dict__}"
