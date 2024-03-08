#!/usr/bin/python3
import json
import os

class FileStorage:
    """
    A class that serializes instances to a JSON file
    and deserializes JSON file to instances
    """
    __file_path = 'file.json'
    __objects = {}

    def all(self):
        """returns the dictionary __objects"""
        return self.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        self.__objects[f'{obj.__class__.__name__}.{obj.id}'] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        with open(self.__file_path, 'w') as file:
            data = {key: value.to_dict() for key, value in self.__objects.items()}
            json.dump(data, file, indent=4)

    def Classes(self):
        from models.base_model import BaseModel
        from models.user import User
        classes = {
            "BaseModel": BaseModel,
            "User": User
        }
        return classes

    def reload(self):
        """deserializes the JSON file to __objects (only if the JSON file (__file_path) exists"""
        if os.path.exists(self.__file_path):
            with open(self.__file_path, 'r') as file:
                data = json.load(file)
                for key, value in data.items():
                    self.__objects[key] = self.Classes()[key[:key.index('.')]](**value)
