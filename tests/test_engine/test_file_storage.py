#!/usr/bin/python3
"""Unittest module for the FileStorage class."""

import unittest
from datetime import datetime
import time
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models import storage
import re
import json
import os


class TestFileStorage(unittest.TestCase):
    """Test cases for FileStorage class"""

    def setUp(self):
        """Sets up test methods."""
        pass

    def tearDown(self):
        """Tears down test methods."""
        self.resetStorage()
        pass

    def resetStorage(self):
        """Resets FileStorage data."""
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_1_new(self):
        """tests the new method in FileStorage"""
        self.resetStorage()
        b = BaseModel()
        formats = f"{b.__class__.__name__}.{b.id}"
        dicts = storage.all()
        self.assertTrue(dicts[formats])


if __name__ == "__main__":
    unittest.main()
