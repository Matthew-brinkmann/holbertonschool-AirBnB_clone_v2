#!/usr/bin/python3
"""Contains DBStorage class"""
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

classes = {
    'BaseModel': BaseModel, 'User': User, 'Place': Place,
    'State': State, 'City': City, 'Amenity': Amenity,
    'Review': Review
}


class DBStorage:
    """MySQL database engine for project"""

    __engine = None
    __session = None

    def __init__(self):
        """ Instantiate DBStorage object """
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(HBNB_MYSQL_USER,
                                              HBNB_MYSQL_PWD,
                                              HBNB_MYSQL_HOST,
                                              HBNB_MYSQL_DB),
                                      pool_pre_ping=True)

        if HBNB_ENV == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        results = []
        __classes = [State, City, User, Place, Review, Amenity]
        if cls is None:
            for c in __classes:
                for result in self.__session.query(c):
                    results.append(result)
        else:
            result = self.__session.query(eval(cls))
            results = result.all()
        # return the results as a dictionary with class.id as key
        return {"{}.{}".format(result.__class__.__name__, result.id): result
                for result in results}
        # new_dict = {}

        # for item in classes:
        #     if cls is None or cls is classes[item] or cls is item:
        #         dbObjects = self.__session.query(classes[item]).all()
        #         for obj in dbObjects:
        #             key = obj.__class__.__name__ + '.' + obj.id
        #             new_dict[key] = obj
        # return new_dict

    def new(self, obj):
        """Adds new object to current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create current database session from the engine
        using a sessionmaker"""
        Base.metadata.create_all(self.__engine)

        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session

    def close(self):
        """Removes session"""
        self.__session.remove()
