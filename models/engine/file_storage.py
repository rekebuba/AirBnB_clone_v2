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
        obj_dict = {}
        for key, value in self.__objects.items():
            if cls:
                if self.__objects[key].__class__ == cls:
                    obj_dict[key] = self.__objects[key]
            else:
                obj_dict[key] = self.__objects[key]
        return obj_dict

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        if hasattr(obj, '_sa_instance_state'):
            delattr(obj, '_sa_instance_state')
        self.__objects[f'{obj.__class__.__name__}.{obj.id}'] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        with open(self.__file_path, 'w') as file:
            data = {k: v.to_dict() for k, v in self.__objects.items()}
            json.dump(data, file)

    def delete(self, obj=None):
        """
        delete obj from __objects if it's inside
        if obj is equal to None, the method should not do anything
        """
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            for key in self.__objects.keys():
                del self.__objects[key]
                break

    def reload(self):
        """deserializes the JSON file to __objects
        (only if the JSON file (__file_path) exists"""
        if os.path.exists(self.__file_path):
            with open(self.__file_path, 'r') as file:
                data = json.load(file)
                for key, value in data.items():
                    A = key.index('.')
                    self.__objects[key] = self.classes()[key[:A]](**value)

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

    def close(self):
        """for deserializing the JSON file to objects """
        self.reload()
