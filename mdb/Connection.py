__author__ = 'plasmashadow'

from pymongo import MongoClient
from mdb.urltools import UrlBuilder


class AbstractConnection(object):
    """
      An Abstract Class for holding connection objects.
    """

    def __init__(self, host=None, username=None, password=None, port=27017, database = None):
        """
        Gets the requested Parameters from the user and establishes the connection to mongodb
        :param host: hostname/public IP Address
        :param username: username for the connection None is not specified
        :param password: password for getting connected to the database
        :param port: Port in which it has to be connected
        :return:
        """
        self._host = host
        self._port = port
        self._user = username
        self._pass = password
        self._db = database
        ub = UrlBuilder(scheme="mongodb",
                        host=self._host,
                        port=self._port,
                        username=self._user,
                        password=self._pass,
                        database=self._db)
        self._connection_url = str(ub)
        self._session = None

    def _connect(self, new=False):
        """
          returns the database session to the user
        :param new: if this paramter is True it returns the new session to the user
        :return:
        """
        if self._session and not new:
            return self._session
        self._session = MongoClient(self._connection_url)
        return self._session






