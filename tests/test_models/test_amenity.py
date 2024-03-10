#!/usr/bin/python3
"""Unittest module for the Amenity class."""

import unittest
from models.base_model import BaseModel
from models.amenity import Amenity
from models.engine.file_storage import FileStorage
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

    def resetStorage(self):
        """Resets amenity data."""
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_instantiation(self):
        """Tests instantiation of Amenity class."""

        b = Amenity()
        self.assertEqual(str(type(b)), "<class 'models.amenity.Amenity'>")
        self.assertIsInstance(b, Amenity)
        self.assertTrue(issubclass(type(b), BaseModel))


if __name__ == '__main__':
    unittest.main()
