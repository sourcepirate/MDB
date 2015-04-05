__author__ = 'plasmashadow'


class Property(object):
    """
      An abstract class for Defining the all other properties.
    """
    def _validate(self, value):
        """
          Used to validate the input value
        :param value: value is data that is been got from the user
        :return:
        """
        pass

    def _store_to_mongo(self, value):
        """
          This method is used to store a value
        :param value:
        :return:
        """
        return str(value)

    def _get_from_mongo(self, value):
        """
          This value gets the data from mongo and returns different format
        :param value:
        :return:
        """
        return str(value)

    def __get__(self, instance, owner):
        """
        Used to assign to a property such that it can be used as a property
        descriptor
        :param instance: current instance
        :param owner:
        :return:
        """
        return self.value

    def __set__(self, instance, value):
        self.value = value



class StringData(Property):
    """
       This is Used to represent a string property
    """
    def __init__(self):
        self._value = ""

    def _validate(self, value):
        """
        Used to validate a string object
        :param value:
        :return:
        """
        if not isinstance(value, str):
            raise TypeError("String data is not assigned to string Field")

    @property
    def value(self):
        return str(self._value)

    @value.setter
    def value(self, value):
        self._validate(value)
        self._value = value

