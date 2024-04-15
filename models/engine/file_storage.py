#!/usr/bin/python3
"""module for File storage"""

import datetime
import json
import os


class FileStorage:
    """
    A class that serializes instances to a JSON file
    and deserializes JSON file to instances
    """
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """returns the dictionary __objects"""
        keys = self.__objects.keys()
        obj_dict = {}
        if cls:
            for key in keys:
                if self.__objects[key].__class__ == cls:
                    obj_dict[key] = self.__objects[key]
            return obj_dict    
        return self.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        self.__objects[f'{obj.__class__.__name__}.{obj.id}'] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        with open(self.__file_path, 'w') as file:
            data = {k: v.to_dict() for k, v in self.__objects.items()}
            json.dump(data, file, indent=4)

    def delete(self, obj=None):
        del self.__objects[f"{obj.__class__.__name__}.{obj.id}"]

    def classes(self):
        """All the classes that are available in one dictionary"""
        from models.base_model import BaseModel
        from models.user import User
        from models.amenity import Amenity
        from models.city import City
        from models.place import Place
        from models.review import Review
        from models.state import State

        classes = {
            "BaseModel": BaseModel,
            "User": User,
            "Amenity": Amenity,
            "City": City,
            "Place": Place,
            "Review": Review,
            "State": State
        }
        return classes

    def reload(self):
        """deserializes the JSON file to __objects
        (only if the JSON file (__file_path) exists"""
        if os.path.exists(self.__file_path):
            with open(self.__file_path, 'r') as file:
                data = json.load(file)
                for key, value in data.items():
                    A = key.index('.')
                    self.__objects[key] = self.classes()[key[:A]](**value)
        else:
            return

    def attributes(self):
        """Returns the valid attributes and their types for classname"""
        attributes = {
            "BaseModel":
                     {"id": str,
                      "created_at": datetime.datetime,
                      "updated_at": datetime.datetime},
            "User":
                     {"email": str,
                      "password": str,
                      "first_name": str,
                      "last_name": str},
            "State":
                     {"name": str},
            "City":
                     {"state_id": str,
                      "name": str},
            "Amenity":
                     {"name": str},
            "Place":
                     {"city_id": str,
                      "user_id": str,
                      "name": str,
                      "description": str,
                      "number_rooms": int,
                      "number_bathrooms": int,
                      "max_guest": int,
                      "price_by_night": int,
                      "latitude": float,
                      "longitude": float,
                      "amenity_ids": list},
            "Review":
            {"place_id": str,
                         "user_id": str,
                         "text": str}
        }
        return attributes
