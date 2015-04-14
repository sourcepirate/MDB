__author__ = 'plasmashadow'

import six
import json
import mdb
from mdb.Property import Property, EmptyProperty
from mdb.Cursor import Cursor
from mdb import notinstancemethod

"""used to check for older dependencies"""
try:
    from pymongo.dbref import DBRef
    from pymongo.objectid import ObjectId
except ImportError:
    from bson.dbref import DBRef
    from bson.objectid import ObjectId

import logging

class BiContextual(object):

    """
       Used to get the values of class from meta object type and
       object name from instance method
    """

    def __init__(self, name):
        self.name = name

    def __get__(self, instance, type=None):

        if instance is None:
            return getattr(type, '_class_'+self.name)
        return getattr(instance, '_instance_'+self.name)

#creating more exceptions

class InvalidUpdate(Exception):
    """
       If a model Tries to update an invalid field
    """
    pass

class UnknownField(Exception):
    """
      If an unknown field is encountered while processing
      all fields on the model.
    """
    pass

class ModelMeta(type):
    """
      This class acts as a MetaClass for all models.
    """

    def __new__(cls, name, bases, attributes):
        attributes["__fields"] = {}
        new_model = super(ModelMeta, cls).__new__(cls, name, bases, attributes)
        new_model._update_fields()
        if hasattr(new_model, "_child_models"):
            new_model._child_models = {}
        return new_model

    def __setattr__(cls, key, value):
        super(ModelMeta, cls).__setattr__(key, value)
        if isinstance(value, Property):
            cls._update_fields()

class Document(dict, six.with_metaclass(ModelMeta)):
    """
      The Base Document Object Centered around the Mongodb model
    """
    _id_field = '_id'
    _id_type = ObjectId
    _name = None
    _collection = None
    _init_okay = False
    __fields = None

    @classmethod
    def new(cls, **kwargs):
        """
          Create a new Model instance with keyword arguments
        :param kwargs:
        :return:
        """
        instance = cls(**kwargs)
        return instance

    @classmethod
    def use(cls, session):
        """
        Wraps the class with specified Connection Session
        :param session:
        :return:
        """
        class Wrapped(cls):
            pass

        Wrapped.__name__ = cls.__name__
        connection = session.connection
        collection = connection.get_connection(Wrapped._get_name())
        Wrapped._collection = collection
        return Wrapped

    @classmethod
    def create(cls, **kwargs):
        """
        Used to Create a new Model instance
        :param kwargs:
        :return:
        """
        _instance = None
        if hasattr(cls, "new"):
            _instance = cls.new(**kwargs)
        else:
            _instance = cls(**kwargs)
        _instance.save()
        return _instance

    def __init__(self, **kwargs):
        """
          Used to Create an Instance of Object without saving it.
        :param kwargs:
        :return:
        """

        super(Document, self).__init__()
        create_fields = self._auto_create_fields
        is_new_instance = self._id_field not in kwargs

        for key, value in kwargs.iteritems():
            if is_new_instance:
                if key in self._fields.values():
                    setattr(self, key, value)
                else:
                    if not create_fields:
                        raise UnknownField("Unknown Field %s"%key)
                    self.add_field(key, Property())
                    setattr(self, key, value)
            else:
                self[key] = value

        for field_name in self._fields.values():
            attr = getattr(self.__class__, field_name)
            self._fields[attr.id] = field_name
            attr._set_default(self, field_name)

    @property
    def _auto_create_fields(self):
        if hasattr(self, "AUTO_CREATE_FIELDS"):
            return self.AUTO_CREATE_FIELDS
        return mdb.AUTO_CREATE_FIELDS

    @property
    def _fields(self):
        """
          Wrapping Property Utility for Property Class
        :return:
        """
        return self.__class__.__fields

    @classmethod
    def _update_fields(cls):
        """
          Used to Update the Fields for models Each time clears the
          Model and reupdates it.
        :return:
        """
        cls.__fields = {}
        for attr_key in dir(cls):
            attr = getattr(cls, attr_key)
            if not isinstance(attr, Property):
                continue
            cls.__fields[attr.id] = attr_key

    @classmethod
    def add_field(cls, field_name, new_field_descriptor):
        """
        Adds a new field on to the class
        :param field_name: name of the field to be added
        :param new_field_descriptor:  new Field Descriptor
        :return:
        """

        setattr(cls, field_name, new_field_descriptor)
        cls._update_fields()

    def _get_id(self):
        """
        Used to get the id of the Model
        :return:
        """
        return self.get(self._id_field)

    def save(self, *args, **kwargs):
        """
        Passed to PyMongo to save after Checking the Values
        :param args:
        :param kwargs:
        :return:
        """
        collection = self._get_collection()
        self._check_required()
        new_object_id = collection.save(self.copy(), *args, **kwargs)
        if not self._get_id():
            super(Document, self).__setattr__(self._id_field, new_object_id)
        return new_object_id

    @classmethod
    def _class_update(cls, *args, **kwargs):
        """
          Used for updating the Model Class
        :param args:
        :param kwargs:
        :return:
        """
        collection = cls._get_collection()
        return collection.update(*args, **kwargs)

    def _instance_update(self):
        """
          Used as wrapper for Pymongo's update
        :return:
        """
        pass







