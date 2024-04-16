#!/usr/bin/python3
"""Module for Base_model"""
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from models import storage
from datetime import datetime
import uuid

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
                if key == "created_at":
                    self.__dict__["created_at"] = datetime.strptime(
                        kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
                elif key == "updated_at":
                    self.__dict__["updated_at"] = datetime.strptime(
                        kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    self.__dict__[key] = value
                setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def save(self):
        """updates the public instance attribute updated_at
        with the current datetime"""
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """
        returns a dictionary containing all key/values of __dict__ of datetime
        """
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = type(self).__name__
        obj_dict['updated_at'] = obj_dict["updated_at"].isoformat()
        obj_dict['created_at'] = obj_dict["created_at"].isoformat()
        try:
            del obj_dict['_sa_instance_state']
        except KeyError:
            pass
        return obj_dict

    def delete(self):
        storage.delete(self)

    def __str__(self):
        """Return a string representation"""
        return f"[{type(self).__name__}] ({self.id}) {self.__dict__}"
