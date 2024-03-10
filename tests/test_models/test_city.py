#!/usr/bin/python3
"""Unittest module for the City class."""

import unittest
from datetime import datetime
import time
from models.base_model import BaseModel
from models.city import City
from models.engine.file_storage import FileStorage
from models import storage
import re
import json
import os


class TestFileStorage(unittest.TestCase):
    """Test cases for City class"""

    def setUp(self):
        """Sets up test methods."""
        pass

    def tearDown(self):
        """Tears down test methods."""
        self.resetStorage()
        pass

def resetStorage(self):
        """Resets city data."""
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)
