__author__ = 'plasmashadow'

from mondb.Cursor import Cursor
from mondb.MongoLogger import Logger
log = Logger()


class OperatorNotSupported(Exception):
    pass

class Query(object):

    def __init__(self, Model):
        self.__opr = {"<=": "$lte", ">=": "$gte", "<": "$lt", ">": "$gt", "!=": "$ne"}
        self.model = Model
        self._start_id = None
        self.cursor = Cursor(self.model)
        self.count = self.model.count()
        self.findstr = {}

    def filter(self, field_name, opr, value):
        """
        Adds filter to a particular category
        :param field_name:
        :param opr:
        :param value:
        :return:
        """
        if opr not in self.__opr:
            raise OperatorNotSupported(opr+" Not supported")
        dst = {self.__opr[opr]: value}
        self.findstr[field_name] = dst



    def fetch(self, offset=None, start_cursor=None):
        """
        Fetch the result of the particular query
        :param offset:
        :param start_cursor:
        :return:
        """

        temp = self.findstr
        self.findstr = {}
        log.info(temp)
        return self.model.find(temp)