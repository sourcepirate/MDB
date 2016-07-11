
from motor.motor_tornado import MotorClient
from tornado.concurrent import return_future
from tornado.gen import engine
from .urltools import UrlBuilder


class Connection(object):
    """
       Connection interface
    """

    _instance = None
    _dbs = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = Connection()
        return cls._instance

    @classmethod
    def connect(cls, db, **kwargs):
        host = kwargs.get("host", "localhost")
        port = kwargs.get("port", 27017)
        scheme = "mongodb"
        username = kwargs.get("username")
        password = kwargs.get("password")
        url = UrlBuilder(scheme=scheme,
                         host=host,
                         port=port,
                         username=username,
                         password=password,
                         database=None)
        url_string = str(url)
        conn = cls.get_instance()
        conn._instance = MotorClient(url_string)
        conn._dbs = getattr(conn._instance, db)
        return conn._instance

    @classmethod
    @return_future
    def is_alive(cls, callback):
        instance = cls.get_instance()._instance
        instance.alive(callback)

    @classmethod
    def get_connection(cls, db):
        instance = cls.get_instance()
        return getattr(instance._instance, db)
