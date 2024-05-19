#!/usr/bin/python3
"""
New engine for data management
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from checker import Checker
from os import getenv
from models.base_model import Base
from models.city import City
from models.state import State
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """ storage engine using SQLAlchemy """
    __engine = None
    __session = None

    def __init__(self):
        """
        create the engine (self.__engine)
        the engine must be linked to the MySQL database
        and user created before (hbnb_dev and hbnb_dev_db)
        """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            getenv('HBNB_MYSQL_USER'),
            getenv('HBNB_MYSQL_PWD'),
            getenv('HBNB_MYSQL_HOST'),
            getenv('HBNB_MYSQL_DB')), pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        query on the current database session
        all objects depending of the cls name
        if cls=None, query all types of objects
        """
        if cls is not None and type(cls) == str:
                cls = eval(cls)
        obj_dict = {}
        checker = Checker()
        classes_dict = checker.classes()
        if cls is None or cls == '':
            for k, c in classes_dict.items():
                if k != 'BaseModel':
                    objs = self.__session.query(c).all()
                    for obj in objs:
                        key = obj.__class__.__name__ + '.' + obj.id
                        obj_dict[key] = obj
        else:
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = obj.__class__.__name__ + '.' + obj.id
                obj_dict[key] = obj
        return obj_dict

    def new(self, obj):
        """
        add the object to the current
        database session (self.__session)
        """
        self.__session.add(obj)
        self.__session.flush()
        self.__session.refresh(obj)

    def save(self):
        """
        commit all changes of the current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        delete from the current database session obj if not None
        """
        self.__session.query(type(obj)).filter(type(obj).id == obj.id).delete()

    def reload(self):
        """
        create all tables in the database
        make sure your Session is thread-safe
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(expire_on_commit=False,
                                       bind=self.__engine)
        self.__session = scoped_session(session_factory)()


    def close(self):
        """closes the current SQLAlchemy Session"""
        self.__session.close()
