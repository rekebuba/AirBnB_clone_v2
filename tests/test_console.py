#!/usr/bin/python3
"""Unittest module for the console class."""

import unittest
from console import HBNBCommand
from unittest.mock import patch
from io import StringIO


class TestConsole(unittest.TestCase):
    """Test cases for user class"""

    def setUp(self):
        """Sets up test methods."""
        pass

    def test_EOF(self):
        """Tests the EOF command"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("EOF")
        msg = f.getvalue()
        self.assertEqual("\n", msg)

    def test_emptyline(self):
        """Test emptyline functionality"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("\n")
        s = ""
        self.assertEqual(s, f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("                  \n")
        s = ""
        self.assertEqual(s, f.getvalue())

    def test_help_1(self):
        """Tests the help command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help")
        s = """
Documented commands (type help <topic>):
========================================
EOF  all  count  create  destroy  help  quit  show  update

"""
        self.assertEqual(s, f.getvalue())

    def test_help_2(self):
        """Tests the help command"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help show")
            output = "Prints the string representation of an instance\n\
        based on the class name and id\n"
            self.assertEqual(output, f.getvalue())

    def test_create_1(self):
        """Test the create command with invalid class"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create class")
            output = "** class doesn't exist **\n"
            self.assertEqual(output, f.getvalue())

    def test_create_2(self):
        """Test the create command with invalid class"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create class")
            output = "** class doesn't exist **\n"
            self.assertEqual(output, f.getvalue())

    def test_show_1(self):
        """tests the show command whit out class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show")
            output = "** class name is missing **\n"
            self.assertEqual(output, f.getvalue())

    def test_show_2(self):
        """tests the show command with invalid class"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show class")
            output = "** class doesn't exist **\n"
            self.assertEqual(output, f.getvalue())

    def test_show_3(self):
        """tests the show command with out id"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show User")
            output = "** instance id missing **\n"
            self.assertEqual(output, f.getvalue())

    def test_show_4(self):
        """tests the show command with invalid id"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show User 1234")
            output = "** no instance found **\n"
            self.assertEqual(output, f.getvalue())

    def test_show_5(self):
        """tests the show command with invalid id"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show User 1234")
            output = "** no instance found **\n"
            self.assertEqual(output, f.getvalue())

    def test_destroy_1(self):
        """tests the show command whit out class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy")
            output = "** class name is missing **\n"
            self.assertEqual(output, f.getvalue())

    def test_destroy_2(self):
        """tests the show command with invalid class"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy class")
            output = "** class doesn't exist **\n"
            self.assertEqual(output, f.getvalue())

    def test_destroy_3(self):
        """tests the show command with out id"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy User")
            output = "** instance id missing **\n"
            self.assertEqual(output, f.getvalue())

    def test_destroy_4(self):
        """tests the show command with invalid id"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy User 1234")
            output = "** no instance found **\n"
            self.assertEqual(output, f.getvalue())

    def test_destroy_5(self):
        """tests the show command with invalid id"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy User 1234")
            output = "** no instance found **\n"
            self.assertEqual(output, f.getvalue())


if __name__ == "__main__":
    unittest.main()
