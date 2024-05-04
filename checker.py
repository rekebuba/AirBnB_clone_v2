#!/usr/bin/python3
""" helper module to keep track of the class and their attributes """
import datetime


class Checker:
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
