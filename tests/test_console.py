#!/usr/bin/python3
"""Module for TestHBNBCommand class."""

import re
import os
import sys
import json
import MySQLdb
import unittest
import datetime
import sqlalchemy
from io import StringIO
from models import storage
from models.user import User
from console import HBNBCommand
from unittest.mock import patch
from tests import clear_stream
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestHBNBCommand(unittest.TestCase):

    """Tests HBNBCommand console."""

    attribute_values = {
        str: "foobar108",
        int: 1008,
        float: 1.08
    }

    reset_values = {
        str: "",
        int: 0,
        float: 0.0
    }

    test_random_attributes = {
        "strfoo": "barfoo",
        "intfoo": 248,
        "floatfoo": 9.8
    }

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db', 'FileStorage test')
    def test_fs_create(self):
        """Tests the create command with the file storage.
        """
        with patch('sys.stdout', new=StringIO()) as cout:
            cons = HBNBCommand()
            cons.onecmd('create City name="Texas"')
            mdl_id = cout.getvalue().strip()
            clear_stream(cout)
            self.assertIn('City.{}'.format(mdl_id), storage.all().keys())
            cons.onecmd('show City {}'.format(mdl_id))
            self.assertIn("'name': 'Texas'", cout.getvalue().strip())
            clear_stream(cout)
            cons.onecmd('create User name="James" age=17 height=5.9')
            mdl_id = cout.getvalue().strip()
            self.assertIn('User.{}'.format(mdl_id), storage.all().keys())
            clear_stream(cout)
            cons.onecmd('show User {}'.format(mdl_id))
            self.assertIn("'name': 'James'", cout.getvalue().strip())
            self.assertIn("'age': 17", cout.getvalue().strip())
            self.assertIn("'height': 5.9", cout.getvalue().strip())

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_create(self):
        """Tests the create command with the database storage.
        """
        with patch('sys.stdout', new=StringIO()) as cout:
            cons = HBNBCommand()
            # creating a model with non-null attribute(s)
            with self.assertRaises(sqlalchemy.exc.OperationalError):
                cons.onecmd('create User')
            # creating a User instance
            clear_stream(cout)
            cons.onecmd('create User email="john25@gmail.com" password="123"')
            mdl_id = cout.getvalue().strip()
            dbc = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = dbc.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(mdl_id))
            result = cursor.fetchone()
            self.assertTrue(result is not None)
            self.assertIn('john25@gmail.com', result)
            self.assertIn('123', result)
            cursor.close()
            dbc.close()

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_show(self):
        """Tests the show command with the database storage.
        """
        with patch('sys.stdout', new=StringIO()) as cout:
            cons = HBNBCommand()
            # showing a User instance
            obj = User(email="john25@gmail.com", password="123")
            dbc = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = dbc.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(obj.id))
            result = cursor.fetchone()
            self.assertTrue(result is None)
            cons.onecmd('show User {}'.format(obj.id))
            self.assertEqual(
                cout.getvalue().strip(),
                '** no instance found **'
            )
            obj.save()
            dbc = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = dbc.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(obj.id))
            clear_stream(cout)
            cons.onecmd('show User {}'.format(obj.id))
            result = cursor.fetchone()
            self.assertTrue(result is not None)
            self.assertIn('john25@gmail.com', result)
            self.assertIn('123', result)
            self.assertIn('john25@gmail.com', cout.getvalue())
            self.assertIn('123', cout.getvalue())
            cursor.close()
            dbc.close()

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_count(self):
        """Tests the count command with the database storage.
        """
        with patch('sys.stdout', new=StringIO()) as cout:
            cons = HBNBCommand()
            dbc = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = dbc.cursor()
            cursor.execute('SELECT COUNT(*) FROM states;')
            res = cursor.fetchone()
            prev_count = int(res[0])
            cons.onecmd('create State name="Enugu"')
            clear_stream(cout)
            cons.onecmd('count State')
            cnt = cout.getvalue().strip()
            self.assertEqual(int(cnt), prev_count + 1)
            clear_stream(cout)
            cons.onecmd('count State')
            cursor.close()
            dbc.close()

    def setUp(self):
        """Sets up test cases."""
        if os.path.isfile("file.json"):
            os.remove("file.json")
        self.resetStorage()

    def resetStorage(self):
        """Resets FileStorage data."""
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_help(self):
        """Tests the help command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help")
        s = """
Documented commands (type help <topic>):
========================================
EOF  all  count  create  destroy  help  quit  show  update

"""
        self.assertEqual(s, f.getvalue())

    def test_do_EOF(self):
        """Tests EOF commmand."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("EOF")
        msg = f.getvalue()
        self.assertTrue(len(msg) == 1)
        self.assertEqual("\n", msg)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("EOF garbage")
        msg = f.getvalue()
        self.assertTrue(len(msg) == 1)
        self.assertEqual("\n", msg)

    def test_emptyline(self):
        """Tests emptyline functionality."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("\n")
        s = ""
        self.assertEqual(s, f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("                  \n")
        s = ""
        self.assertEqual(s, f.getvalue())

    def test_do_create(self):
        """Tests create for all classes."""
        for classname in self.classes():
            self.help_test_do_create(classname)

    def help_test_do_create(self, classname):
        """Helper method to test the create commmand."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create {}".format(classname))
        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)
        key = "{}.{}".format(classname, uid)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all {}".format(classname))
        self.assertTrue(uid in f.getvalue())

    def test_do_create_error(self):
        """Tests create command with errors."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create garbage")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

    def test_do_show(self):
        """Tests show for all classes."""
        for classname in self.classes():
            self.help_test_do_show(classname)
            self.help_test_show_advanced(classname)

    def help_test_do_show(self, classname):
        """Helps test the show command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create {}".format(classname))
        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show {} {}".format(classname, uid))
        s = f.getvalue()[:-1]
        self.assertTrue(uid in s)

    def test_do_show_error(self):
        """Tests show command with errors."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show garbage")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show BaseModel")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show BaseModel 6524359")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** no instance found **")

    def help_test_show_advanced(self, classname):
        """Helps test .show() command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create {}".format(classname))
        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, uid))
        s = f.getvalue()
        self.assertTrue(uid in s)

    def test_do_show_error_advanced(self):
        """Tests show() command with errors."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(".show()")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("garbage.show()")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.show()")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('BaseModel.show("6524359")')
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** no instance found **")

    def test_do_destroy(self):
        """Tests destroy for all classes."""
        for classname in self.classes():
            self.help_test_do_destroy(classname)
            self.help_test_destroy_advanced(classname)

    def help_test_do_destroy(self, classname):
        """Helps test the destroy command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create {}".format(classname))
        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy {} {}".format(classname, uid))
        s = f.getvalue()[:-1]
        self.assertTrue(len(s) == 0)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(".all()")
        self.assertFalse(uid in f.getvalue())

    def test_do_destroy_error(self):
        """Tests destroy command with errors."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy garbage")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy BaseModel")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy BaseModel 6524359")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** no instance found **")

    def help_test_destroy_advanced(self, classname):
        """Helps test the destroy command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create {}".format(classname))
        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('{}.destroy("{}")'.format(classname, uid))
        s = f.getvalue()[:-1]
        self.assertTrue(len(s) == 0)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(".all()")
        self.assertFalse(uid in f.getvalue())

    def test_do_destroy_error_advanced(self):
        """Tests destroy() command with errors."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(".destroy()")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("garbage.destroy()")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.destroy()")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('BaseModel.destroy("6524359")')
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** no instance found **")

    def test_do_all(self):
        """Tests all for all classes."""
        for classname in self.classes():
            self.help_test_do_all(classname)
            self.help_test_all_advanced(classname)

    def help_test_do_all(self, classname):
        """Helps test the all command."""
        uid = self.create_class(classname)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all")
        s = f.getvalue()[:-1]
        self.assertTrue(len(s) > 0)
        self.assertIn(uid, s)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all {}".format(classname))
        s = f.getvalue()[:-1]
        self.assertTrue(len(s) > 0)
        self.assertIn(uid, s)

    def test_do_all_error(self):
        """Tests all command with errors."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all garbage")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

    def help_test_all_advanced(self, classname):
        """Helps test the .all() command."""
        uid = self.create_class(classname)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("{}.all()".format(classname))
        s = f.getvalue()[:-1]
        self.assertTrue(len(s) > 0)
        self.assertIn(uid, s)

    def test_do_all_error_advanced(self):
        """Tests all() command with errors."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("garbage.all()")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

    def test_count_all(self):
        """Tests count for all classes."""
        for classname in self.classes():
            self.help_test_count_advanced(classname)

    def help_test_count_advanced(self, classname):
        """Helps test .count() command."""
        for i in range(20):
            uid = self.create_class(classname)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("{}.count()".format(classname))
        s = f.getvalue()[:-1]
        self.assertTrue(len(s) > 0)
        self.assertEqual(s, "20")

    def test_do_count_error(self):
        """Tests .count() command with errors."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("garbage.count()")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(".count()")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

    def test_update_1(self):
        """Tests update 1..."""
        classname = "BaseModel"
        attr = "foostr"
        val = "fooval"
        uid = self.create_class(classname)
        cmd = '{}.update("{}", "{}", "{}")'
        #  cmd = 'update {} {} {} {}'
        cmd = cmd.format(classname, uid, attr, val)
        #  print("CMD::", cmd)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(cmd)
        s = f.getvalue()
        self.assertEqual(len(s), 0)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, uid))
        s = f.getvalue()
        self.assertIn(attr, s)
        self.assertIn(val, s)

    def test_update_2(self):
        """Tests update 1..."""
        classname = "User"
        attr = "foostr"
        val = "fooval"
        uid = self.create_class(classname)
        cmd = '{}.update("{}", "{}", "{}")'
        #  cmd = 'update {} {} {} {}'
        cmd = cmd.format(classname, uid, attr, val)
        #  print("CMD::", cmd)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(cmd)
        s = f.getvalue()
        self.assertEqual(len(s), 0)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, uid))
        s = f.getvalue()
        self.assertIn(attr, s)
        self.assertIn(val, s)

    def test_update_3(self):
        """Tests update 1..."""
        classname = "City"
        attr = "foostr"
        val = "fooval"
        uid = self.create_class(classname)
        cmd = '{}.update("{}", "{}", "{}")'
        #  cmd = 'update {} {} {} {}'
        cmd = cmd.format(classname, uid, attr, val)
        #  print("CMD::", cmd)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(cmd)
        s = f.getvalue()
        self.assertEqual(len(s), 0)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, uid))
        s = f.getvalue()
        self.assertIn(attr, s)
        self.assertIn(val, s)

    def test_update_4(self):
        """Tests update 1..."""
        classname = "State"
        attr = "foostr"
        val = "fooval"
        uid = self.create_class(classname)
        cmd = '{}.update("{}", "{}", "{}")'
        #  cmd = 'update {} {} {} {}'
        cmd = cmd.format(classname, uid, attr, val)
        #  print("CMD::", cmd)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(cmd)
        s = f.getvalue()
        self.assertEqual(len(s), 0)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, uid))
        s = f.getvalue()
        self.assertIn(attr, s)
        self.assertIn(val, s)

    def test_update_5(self):
        """Tests update 1..."""
        classname = "Amenity"
        attr = "foostr"
        val = "fooval"
        uid = self.create_class(classname)
        cmd = '{}.update("{}", "{}", "{}")'
        #  cmd = 'update {} {} {} {}'
        cmd = cmd.format(classname, uid, attr, val)
        #  print("CMD::", cmd)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(cmd)
        s = f.getvalue()
        self.assertEqual(len(s), 0)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, uid))
        s = f.getvalue()
        self.assertIn(attr, s)
        self.assertIn(val, s)

    def test_update_6(self):
        """Tests update 1..."""
        classname = "Review"
        attr = "foostr"
        val = "fooval"
        uid = self.create_class(classname)
        cmd = '{}.update("{}", "{}", "{}")'
        #  cmd = 'update {} {} {} {}'
        cmd = cmd.format(classname, uid, attr, val)
        #  print("CMD::", cmd)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(cmd)
        s = f.getvalue()
        self.assertEqual(len(s), 0)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, uid))
        s = f.getvalue()
        self.assertIn(attr, s)
        self.assertIn(val, s)

    def test_update_7(self):
        """Tests update 1..."""
        classname = "Place"
        attr = "foostr"
        val = "fooval"
        uid = self.create_class(classname)
        cmd = '{}.update("{}", "{}", "{}")'
        #  cmd = 'update {} {} {} {}'
        cmd = cmd.format(classname, uid, attr, val)
        #  print("CMD::", cmd)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(cmd)
        s = f.getvalue()
        self.assertEqual(len(s), 0)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, uid))
        s = f.getvalue()
        self.assertIn(attr, s)
        self.assertIn(val, s)

    def test_update_everything(self):
        """Tests update command with errthang, like a baws."""
        for classname, cls in self.classes().items():
            uid = self.create_class(classname)
            for attr, value in self.test_random_attributes.items():
                if type(value) is not str:
                    pass
                quotes = (type(value) == str)
                self.help_test_update(classname, uid, attr,
                                      value, quotes, False)
                self.help_test_update(classname, uid, attr,
                                      value, quotes, True)
            pass
            if classname == "BaseModel":
                continue
            for attr, attr_type in self.attributes()[classname].items():
                if attr_type not in (str, int, float):
                    continue
                self.help_test_update(classname, uid, attr,
                                      self.attribute_values[attr_type],
                                      True, False)
                self.help_test_update(classname, uid, attr,
                                      self.attribute_values[attr_type],
                                      False, True)

    def help_test_update(self, classname, uid, attr, val, quotes, func):
        """Tests update commmand."""
        #  print("QUOTES", quotes)
        FileStorage._FileStorage__objects = {}
        if os.path.isfile("file.json"):
            os.remove("file.json")
        uid = self.create_class(classname)
        value_str = ('"{}"' if quotes else '{}').format(val)
        if func:
            cmd = '{}.update("{}", "{}", {})'
        else:
            cmd = 'update {} {} {} {}'
        cmd = cmd.format(classname, uid, attr, value_str)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(cmd)
        msg = f.getvalue()[:-1]
        # print("MSG::", msg)
        # print("CMD::", cmd)
        self.assertEqual(len(msg), 0)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, uid))
        s = f.getvalue()
        self.assertIn(str(val), s)
        self.assertIn(attr, s)

    def test_do_update_error(self):
        """Tests update command with errors."""
        uid = self.create_class("BaseModel")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update garbage")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update BaseModel")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update BaseModel 6534276893")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** no instance found **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('update BaseModel {}'.format(uid))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** attribute name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('update BaseModel {} name'.format(uid))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** value missing **")

    def test_do_update_error_advanced(self):
        """Tests update() command with errors."""
        uid = self.create_class("BaseModel")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(".update()")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("garbage.update()")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.update()")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.update(6534276893)")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** no instance found **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('BaseModel.update("{}")'.format(uid))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** attribute name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('BaseModel.update("{}", "name")'.format(uid))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** value missing **")

    def create_class(self, classname):
        """Creates a class for console tests."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create {}".format(classname))
        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)
        return uid

    def help_load_dict(self, rep):
        """Helper method to test dictionary equality."""
        rex = re.compile(r"^\[(.*)\] \((.*)\) (.*)$")
        res = rex.match(rep)
        self.assertIsNotNone(res)
        s = res.group(3)
        s = re.sub(r"(datetime\.datetime\([^)]*\))", "'\\1'", s)
        d = json.loads(s.replace("'", '"'))
        return d

    def classes(self):
        """Returns a dictionary of valid classes and their references."""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        classes = {"BaseModel": BaseModel,
                   "User": User,
                   "State": State,
                   "City": City,
                   "Amenity": Amenity,
                   "Place": Place,
                   "Review": Review}
        return classes

    def attributes(self):
        """Returns the valid attributes and their types for classname."""
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


if __name__ == "__main__":
    unittest.main()
