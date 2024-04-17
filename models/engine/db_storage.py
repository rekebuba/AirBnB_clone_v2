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
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            "hbnb_dev", "hbnb_dev_pwd", "localhost", "hbnb_dev_db"), pool_pre_ping=True)
            # getenv('HBNB_MYSQL_USER'),
            # getenv('HBNB_MYSQL_PWD'),
            # getenv('HBNB_MYSQL_HOST'),
            # getenv('HBNB_MYSQL_DB')), pool_pre_ping=True)
            
        # Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        dct = {}
        checker = Checker()
        classes_dict = checker.classes()
        if cls is None or cls == '':
            for k, c in classes_dict.items():
                if k != 'BaseModel':
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
        self.__session.query(type(obj)).filter(type(obj).id == obj.id).delete()

    def reload(self):
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(expire_on_commit=False, bind=self.__engine)
        self.__session = scoped_session(session_factory)()
