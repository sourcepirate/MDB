__author__ = 'plasmashadow'

import six
import json
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

class Document(Model):
    fieldes = {}

    @classmethod
    def _construct_fields(cls):
        """
        This is used to construct all the fields and appropriate value
        :return:
        """
        cls.fieldes = {}
        for attribute in cls.attrs:
            if not isinstance(cls.attrs[attribute], Property):
                continue
            cls.fieldes[attribute] = cls.attrs[attribute].value

    @classmethod
    def save(cls):
        """
          Save method saves the object and returns the id of saved object
        :return: id which represents the primary key.
        """
        cls._construct_fields()
        driver = getattr(cls, '__connection__')
        collection = getattr(driver, cls.__name__)
        id = collection.insert(cls.fieldes)
        return id

    @classmethod
    def delete(cls):
        id = cls.fieldes['_id']
        driver = getattr(cls, '__connection__')
        collection = getattr(driver, cls.__name__)
        g = collection.remove({'_id': id})
        return g

    @classmethod
    def get_by_id(cls, id):
        pass










