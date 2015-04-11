__author__ = 'plasmashadow'

import six
import json
from Property import Property
from bson.objectid import ObjectId



class ModelMeta(type):
    """
    Meta class for all Mongodb models
    """
    def __new__(cls, name, bases, attrs):
        return super(ModelMeta, cls).__new__(cls, name, bases, attrs)

    def __init__(self , name, bases, attrs):
        super(ModelMeta, self).__init__(name, bases, attrs)
        self.attrs = attrs
        self.connection = attrs.get('__connection__')



class Model(six.with_metaclass(ModelMeta)):
    """
       Model dervided from metaclass has all the basic primitive functions
    """
    pass

class Document(Model):


    def _construct(self):
        self.fields = {}
        {self.fields.update({x: self.attrs[x].value}) \
         for x in self.attrs \
         if isinstance(self.attrs[x], Property)}


    def save(self):
        self._construct()
        collection = getattr(self.connection, self.__class__.__name__)
        if self.fields.get("_id"):
            id = collection.insert(self.fields)
            return id
        self.fields.update({'_id': ObjectId(id)})
        print self.fields
        return id

    def key(self):
        return self.fields['_id']

    def delete(self):
        collection = getattr(self.connection, self.__class__.__name__)
        try:
            id = collection.remove({'_id': self.fields["_id"]})
            return id
        except Exception as e:
            raise Exception("Cannot delete Object before persisting")

    def to_dict(self):
        return json.dumps(self.fields)














