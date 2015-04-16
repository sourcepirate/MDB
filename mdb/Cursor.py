__author__ = 'plasmashadow'


from pymongo.cursor import Cursor as MongoCursor
from pymongo import ASCENDING, DESCENDING

ASC = ASCENDING
DSC = DESCENDING

class Cursor(MongoCursor):

    """
       This is just to Cursor to Query Objects on Mongodb with offset
       Provides More functions.
    """

    def __init__(self, model, spec=None, *args, **kwargs):
        """
        Constructor to Initialize the Cursor Class
        :param model: Model on which the cursor is called
        :param spec:
        :param args:
        :param kwargs:
        :return:
        """
        self._order_entities = []
        self._query = spec
        self._model = model
        MongoCursor.__init__(self, model._get_collection(), spec, *args, **kwargs)

    def next(self):
        """
          Get the next element and returns that
          as a model
        :return:
        """
        value = MongoCursor.next(self)
        return self._model(**value)

    def __getitem__(self, *args, **kwargs):
        """
        Simple getter for Cursor Objects
        :param args:
        :param kwargs:
        :return:
        """
        value = MongoCursor.__getitem__(self, *args, **kwargs)
        if type(value) == self.__class__:
            return value
        return self._model(**value)

    def first(self):
        """
         Returns the First Element
        :return:
        """
        if self.count() == 0:
            return None
        return self[0]

    def order(self, **kwargs):
        """
          Order the values of the element
        :param kwargs:
        :return:
        """
        if len(kwargs) is not 1:
            raise TypeError(" order() requires only one argument")
        for key, value in kwargs.iteritems():
            if value not in [ASC, DSC]:
                raise TypeError("Order value must be either ASC for Ascending and DSC for descending")
            self._order_entities.append((key,value))
            self.sort(self._order_entities)
        return self

    def update(self, modifier):
        """
        Used to update the model value
        :param modifier:
        :return:
        """
        if self._query is None:
            raise ValueError("Cannot Update on Query without Value")
        self._model.update(self._query, modifier, multi=True)
        return self

    def change(self, **kwargs):
        modifier = {"$set": kwargs}
        print modifier
        return self.update(modifier)
