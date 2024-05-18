#!/usr/bin/python3
"""__init__ package"""
from os import getenv, environ

# environ['HBNB_MYSQL_USER'] = 'hbnb_dev'
# environ['HBNB_MYSQL_PWD'] = 'hbnb_dev_pwd'
# environ['HBNB_MYSQL_HOST'] = 'localhost'
# environ['HBNB_MYSQL_DB'] = 'hbnb_dev_db'
# environ['HBNB_TYPE_STORAGE'] = 'db'


storage_type = getenv('HBNB_TYPE_STORAGE')
if storage_type == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
