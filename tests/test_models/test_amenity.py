#!/usr/bin/python3
"""Unittest module for the Amenity class."""

import unittest
from datetime import datetime
import time
from models.base_model import BaseModel
from models.amenity import Amenity
from models.engine.file_storage import FileStorage
from models import storage
import re
import json
import os


class TestFileStorage(unittest.TestCase):
    """Test cases for Amenity class"""

    def setUp(self):
        """Sets up test methods."""
        pass

    def tearDown(self):
        """Tears down test methods."""
        self.resetStorage()
        pass
