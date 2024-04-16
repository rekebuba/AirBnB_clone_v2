from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from checker import Checker
import os

class DBStorage:
    cities = relationship("City", backref="state", cascade="all, delete")
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            "hbnb_dev", "hbnb_dev_pwd", "localhost", "hbnb_dev_db"), pool_pre_ping=True)
            # os.getenv('HBNB_MYSQL_USER'),
            # os.getenv('HBNB_MYSQL_PWD'),
            # os.getenv('HBNB_MYSQL_HOST'),
            # os.getenv('HBNB_MYSQL_DB')), pool_pre_ping=True)

    def all(self, cls=None):
        dct = {}
        checker = Checker()
        classes_dict = checker.classes()
        if cls is None:
            for c in classes_dict.values():
                objs = self.__session.query(c).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    dct[key] = obj
        else:
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = obj.__class__.__name__ + '.' + obj.id
                dct[key] = obj
        return dct

    def new(self, obj):
        self.__session.add(obj)
        self.__session.flush()
        self.__session.refresh(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        del self.__session.obj

    def reload(self):
        from models.base_model import BaseModel, Base
        from models.city import City
        from models.state import State
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(expire_on_commit=False, bind=self.__engine))
