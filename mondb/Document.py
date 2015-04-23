__author__ = 'plasmashadow'

import six
import json
import mondb
from mondb.Property import Property, EmptyProperty
from mondb.Cursor import Cursor
from mondb.Connection import Connection
from mondb.Decorators import notinstancemethod
from mondb.Decorators import deprecated

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

class Document(six.with_metaclass(ModelMeta, dict)):

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
            self._fields[attr._id] = field_name
            attr._set_default(self, field_name)

    @property
    def _auto_create_fields(self):
        """
           Auto Create Fields.
           Consider a Model class having the following definition
          >>> class Management(mondb.Document):
          >>>    name = mondb.StringProperty()
          >>>
          >>>m = Management()
          >>>m.age = 23
          Since age is not in the Management Model we cannot assign it
          But by setting the AutoCreate Fields to True we can achive this.
        :return:
        """
        if hasattr(self, "AUTO_CREATE_FIELDS"):
            return self.AUTO_CREATE_FIELDS
        return mondb.AUTO_CREATE_FIELDS

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
            cls.__fields[attr._id] = attr_key

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
            self[self._id_field] = new_object_id
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

    def _instance_update(self,*args, **kwargs):
        """
          Used as wrapper for Pymongo's update
        :return:
        """
        object_id = self._get_id()
        if not object_id:
            raise InvalidUpdate("Invalid Update Call")
        spec = {self._id_field: object_id}
        pass_kwargs = {}
        if "safe" in kwargs:
            pass_kwargs["safe"] = kwargs.pop("safe")
        body = {}
        checks = []
        for key, value in kwargs.iteritems():
            if key in self._fields.values():
                setattr(self, key, value)
            else:
                self[key] = value
            checks.append(key)
            field = getattr(self.__class__, key)
            field_name = field._get_field_name(self)
            body[field_name] = self[field_name]
            logging.debug("Checking fields (%s).", checks)
            self._check_required(*checks)
            collection = self._get_collection()
            #mongodb uses set to store the body of mongodb collections
            return collection.update(spec, {"$set": body}, **pass_kwargs)


    update = BiContextual("update")

    def _check_required(self, *field_names):
        """
          The field uses required to mark the mandatory
          fields. So we need to check if all the required
          fields are been present.
        :return:
        """
        if not field_names:
            field_names = self._fields.values()

        for field_name in field_names:

            field_value = getattr(self.__class__, field_name)
            #the name on what it is stored on mongodb
            storage_name = field_value._get_field_name(self)
            if storage_name not in self:
                if field_value.requried:
                    raise EmptyProperty("Required property is left empyty %s"%storage_name)

    def delete(self, *args, **kwargs):
        """
        Used to Remove a model
        :param args:
        :param kwargs:
        :return:
        """
        if not self._get_id():
            raise ValueError("No id has been set so removel is impossible")
        collection = self._get_collection()
        return self.remove(self._get_id(), *args, **kwargs)

    @notinstancemethod
    def remove(cls, *args, **kwargs):
        """
         Just a Wrapper Around the Collection Remove
        :return:
        """
        if not args:
            raise ValueError("Remove requires an Object to be passed to it")
        collection = cls._get_collection()
        return collection.remove(*args, **kwargs)

    @notinstancemethod
    def drop(cls, *args, **kwargs):
        """
          Just a Wrapper around Pymongo Drop
        :param cls:
        :param args:
        :param kwargs:
        :return:
        """
        if not args:
             raise ValueError("Remove requires an Object to be passed to it")
        collection = cls._get_collection()
        return collection.drop(*args, **kwargs)

    @property
    def id(self):
        return self._get_id()

    _id = id

    @classmethod
    def find(cls, *args, **kwargs):
        """
        Its just a wrapper for collection find -one
        :type kwargs: object
        :param args:
        :param kwargs:
        :return:
        """
        if kwargs and not args:
            raise ValueError("Find One need to get Proper key value pair for querying")

        return Cursor(cls, *args, **kwargs)

    @classmethod
    def find_one(cls, *args, **kwargs):
        """
        Its just a wrapper for collection find -one
        :param args:
        :param kwargs:
        :return:
        """
        if kwargs and not args:
            raise ValueError("Find One need to get Proper key value pair for querying")
        collection = cls._get_collection()
        result = collection.find_one(*args, **kwargs)
        if result:
            result = cls(**result)
        return result


    @classmethod
    def group(cls, *args, **kwargs):
        """
        Its just a wrapper for Pymong Group
        :param args:
        :param kwargs:
        :return:
        """
        return cls._get_collection().group(*args, **kwargs)

    @classmethod
    def search(cls, *args, **kwargs):
        """
        Used to search
        :param kwargs:
        :return:
        """
        query = {}
        for key, value in kwargs.iteritems():

            if isinstance(key, Document):
                # used to get the reference model
                value = value._get_ref()
            field = getattr(cls, key)
            if field._field_name:
                key = field._field_name

            query[key] = value
        return cls.find(query)

    @classmethod
    def search_or_create(cls, **kwargs):
        """
        Search for the instance that matches with kwargs
        else creates it
        :param kwargs:
        :return:
        """
        obj = cls.search(**kwargs).first()
        if obj:
            return obj
        return cls.create(**kwargs)

    @classmethod
    def first(cls, **kwargs):
        """
        Returns the first matching occurance
        :param kwargs:
        :return:
        """
        return cls.search(**kwargs).first()

    @classmethod
    def grap(cls, objectid):
        """
        Used to Retrive the key id
        :param objectid:
        :return:
        """
        if type(objectid) != cls._id_type:
            objectid = cls._id_type(objectid)
        return cls.find_one({cls._id_field: objectid})

    @classmethod
    def create_index(cls, *args, **kwargs):
        return cls._get_collection().create_index(*args, **kwargs)


    @classmethod
    def ensure_index(cls, *args, **kwargs):
        return cls._get_collection().ensure_index(*args, **kwargs)

    @classmethod
    def drop_indexes(cls, *args, **kwargs):
        return cls._get_collection().drop_indexes(*args, **kwargs)

    @classmethod
    def distinct(cls, key):
        return cls.find().distinct(key)

    @classmethod
    def _get_collection(cls):
        """
        Used to get the collection from Mongodb Connection object
        :return:
        """
        if not cls._collection:
            conn = Connection.get_instance()
            collection = conn.get_collection(cls._get_name())
            cls._collection = collection
        return cls._collection

    @classmethod
    def _get_name(cls):
        """
        Retrieves the collection name.
        Overwrite _name to set it manually.
        """
        if cls._name:
            return cls._name
        return cls.__name__.lower()

    def __eq__(self, other):

        my_id = self._get_id()
        that_id = other._get_id()
        if self._get_name() == other._get_name() and that_id and my_id and that_id ==my_id:
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)


    @classmethod
    def count(cls):
        return cls.find().count()

    @notinstancemethod
    def make_ref(cls, idval):
        """ Generates a DBRef for a given id. """
        if type(idval) != cls._id_type:
            # Casting to ObjectId (or str, or whatever is configured)
            idval = cls._id_type(idval)
        return DBRef(cls._get_name(), idval)

    def get_ref(self):
        """ Returns a DBRef for an document. """
        return DBRef(self._get_name(), self._get_id())

    def __unicode__(self):
        """ Returns string representation. Overwrite in custom models. """
        return "<MogoModel:%s id:%s>" % (self._get_name(), self._get_id())

    def __repr__(self):
        """ Just points to __unicode__ """
        return self.__unicode__()

    def __str__(self):
        """ Just points to __unicode__ """
        return self.__unicode__()















