#!/usr/bin/python3
from models import base_model
import json
import os

class FileStorage(BaseModel):
    """
    A class that serializes instances to a JSON file
    and deserializes JSON file to instances
    """
    def __init__(self):
        self.__file_path = 'file.json'
        self.__objects = {}

    def all(self):
        """returns the dictionary __objects"""
        return self.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        self.__objects['key'] = obj.id
        pass

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        with open(self.__file_path, 'w') as file:
            json.dump(self.__objects, file)
        pass

    def reload(self):
        """deserializes the JSON file to __objects (only if the JSON file (__file_path) exists"""
        if os.path.exists(self.__file_path):
            with open(self.__file_path, 'r') as file:
                data = json.load(file)
        pass
