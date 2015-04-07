__author__ = 'plasmashadow'

import six

from Property import Property

class ModelMeta(type):
    """
    Meta class for all Mongodb models
    """
    def __new__(cls, name, bases, attrs):
        cls.attrs = attrs
        return super(ModelMeta, cls).__new__(cls, name, bases, attrs)


class Model(six.with_metaclass(ModelMeta)):
    """
       Model dervided from metaclass has all the basic primitive functions
    """
    @classmethod
    def save(cls):
        """
         Used to save a document
        :return:
        """
        pass

    @classmethod
    def delete(cls):
        """
        Used to delete a document
        :return:
        """
        pass

    @classmethod
    def get(cls, id):
        """
        Used to get a document based on id
        :param id:
        :return:
        """
        pass
from Connection import _engine_connection
class Document(Model):
    fields = {}
    driver = _engine_connection

    @classmethod
    def _construct_fields(cls):
        """
        This is used to construct all the fields and appropriate value
        :return:
        """
        for attribute in cls.attrs:
            if not isinstance(cls.attrs[attribute], Property):
                continue
            cls.fields[attribute] = cls.attrs[attribute].value

    @classmethod
    def save(cls):
        cls._construct_fields()









