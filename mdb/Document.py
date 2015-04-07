__author__ = 'plasmashadow'

import six

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
        pass

    @classmethod
    def delete(cls):
        pass

    @classmethod
    def get(cls, id):
        pass

