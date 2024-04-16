#!/usr/bin/python3
"""module for File storage"""

import datetime
import json
import os
from checker import Checker


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

    def reload(self):
        """deserializes the JSON file to __objects
        (only if the JSON file (__file_path) exists"""
        if os.path.exists(self.__file_path):
            with open(self.__file_path, 'r') as file:
                data = json.load(file)
                for key, value in data.items():
                    A = key.index('.')
                    self.__objects[key] = Checker().classes()[key[:A]](**value)
        else:
            return
