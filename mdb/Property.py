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



class Data(Property):

    def __init__(self):
        self._value = None

    def _validate(self, value):
        pass

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._validate(value)
        self._value = value





class StringData(Data):
    """
       This is Used to represent a string property
    """

    def _validate(self, value):
        """
        Used to validate a string object
        :param value:
        :return:
        """
        if not isinstance(value, str):
            raise TypeError("String data is not assigned to string Field")



class IntegerData(Data):

    """
       This is used to represt the integer data stored on to the
       mongodb
    """
    def _validate(self, value):
        """
          Trying to validate whether the data is integer or not
        :param value:
        :return:
        """
        if not isinstance(value, int):
            raise TypeError("Invalid Integer data")


class ListData(Data):
    """
       This is used to represent the list data value
    """

    def _validate(self, value):
        """
          Trying to validate the list object
        :param value:
        :return:
        """
        if not isinstance(value, list):
            raise TypeError("Invalid List data")






