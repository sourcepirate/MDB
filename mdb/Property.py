__author__ = 'plasmashadow'

try:
    from pymongo.dbref import DBRef
except ImportError:
    from bson.dbref import DBRef


class EmptyProperty(Exception):
    pass




