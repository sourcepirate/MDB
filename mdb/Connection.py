__author__ = 'plasmashadow'

from pymongo.connection import Connection as MongoConnection
from pymongo.errors import ConnectionFailure
from mdb.urltools import UrlBuilder


class Connection(object):
    """
    Acts as a connection Class
    """
    _instance = None
    _connection = None
    _dbs  = None
    _session = None

    @classmethod
    def get_instance(cls):
        """
        Acts as a singleton to get the connection object
        :return:
        """
        if not cls._instance:
            cls._instance = Connection()
        return cls._instance

    @classmethod
    def connect(cls, database=None, *args, **kwargs ):
        if not kwargs.get("host"):
            raise TypeError("Host should be specified")

        host = kwargs.get("host")
        port = kwargs.get("port") if kwargs.get("port") else 27017
        scheme = "mongodb"
        username = kwargs.pop("username") if kwargs.get("username") else None
        password = kwargs.pop("password") if kwargs.get("password") else None
        url = UrlBuilder(scheme=scheme, host=host, port=port, username=username, password=password, database = None)
        url_string = str(url)
        conn = cls.get_instance()
        conn._connection = MongoConnection(*args, **kwargs)
        conn._dbs = database
        return conn._connection

    def get_connection(self, dbstring):
        if not self._connection:
            raise ConnectionFailure("No connection to db")
        if not dbstring:
            if not self._dbs:
                raise TypeError("Database should be specified")
            database = self._dbs
        else:
            database = dbstring
        return self._connection[database]

    def get_collection(self, collection, database):
        return self.get_connection(database=database)[collection]

class Transaction(object):

    def __init__(self, database , *args, **kwargs):
        """
        Stores for transaction
        :param database:
        :param args:
        :param kwargs:
        :return:
        """
        self.database = database
        self.connection = None
        self.args = args
        self.kwargs = kwargs

    def connect(self):
        connection = Connection()
        connection._dbs = self.database
        connection._connection = MongoConnection(*self.args, **self.kwargs)
        self.connection = connection

    def disconnect(self):
        self.connection._connection.disconnect()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

def create_engine(*args,**kwargs):
    return Connection.connect(*args, **kwargs)


def session(database, *args, **kwargs):
    return Transaction(database, *args, **kwargs)














