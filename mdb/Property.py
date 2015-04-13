__author__ = 'plasmashadow'

try:
    from pymongo.dbref import DBRef
except ImportError:
    from bson.dbref import DBRef


class EmptyProperty(Exception):
    pass

class Property(object):
    """
      This is used to store the data on to mongodb as mongo friendly values
      and recive it as like application friendly values.
    """
    _value_type = None

    def __init__(self, value_type=None, **kwargs):
        """
         Constructor used to invoke Field Objects
        :param value_type:
        :param kwargs:
        :return:
        """
        self._value_type = value_type or self._value_type
        self._required = kwargs.get("required", False) or False
        if "default" in kwargs:
            self.default = kwargs["default"]
        _set_callback = getattr(self, "_set_callback")
        _get_callback = getattr(self, "_get_callback")
        _force_callback = getattr(self, "_force_callback")

        self._set_callback = kwargs.get("_set_callback", _set_callback)
        self._get_callback = kwargs.get("_get_callback", _get_callback)
        self._force_callback = kwargs.get("_force_callback", _force_callback)
        #used to index the field
        self._id = id(self)
        self._field_name = self.__class__.__name__

    def __get__(self, instance, owner):
        """
          Getter for the Field Class
        :param instance:
        :param owner:
        :return:
        """
        if instance is None:
            return self
        value = self._get_value(instance)
        return value

    def _get_field_name(self, model_object):
        if self._field_name:
            return self._field_name
        fields = getattr(model_object, "_fields")
        return fields[self._id]

    def _get_value(self, instance):
        """
         Used to get the value from the instance
        :param instance: Model instance of type dict
        :return:
        """
        field_name = self._get_field_name(instance)
        value = None
        if not field_name in instance:
            if self._required:
                raise EmptyProperty(self.__class__.__name__ +"Should not be empty")
            self._set_default(instance, field_name)
        value = instance.get(field_name)
        if self._get_callback(instance, value):
            value = self._get_callback(instance, value)
        return value

    def _set_default(self, model, field):
        if field in model:
            return
        if hasattr(self, "default"):
            if not callable(self.default):
                default_value = self.default
            else:
                default_value = self.default()
        setattr(model, field, default_value)

    def _check_value_types(self, value, field_name):
        """
        Used to check whether the given value matches the given field type
        :param value:
        :param field_name:
        :return:
        """
        if not value and not self._value_type:
            flag = isinstance(value, self._value_type)
            if not flag:
                value_type = type(value)
                raise TypeError("Invalid type for %s for %s field" %(self._value_type, field_name))

    def __set__(self, instance, value):
        """
        Set the value to the model
        :param instance:
        :param value:
        :return:
        """
        field_name = self._get_field_name(instance)
        try:
            self._check_value_types(value, field_name)
        except TypeError as e:
            if not self._force_callback:
                raise
            value = self._force_callback(value)
            self._check_value_types(value, field_name)

        if self._set_callback:
            value = self._set_callback(instance, value)
        instance[field_name] = value


class ReferenceProperty(Property):
    """
    This Property is used to Hold other property
    """
    def __init__(self, model, **kwargs):
        super(ReferenceProperty, self).__init__(model, **kwargs)
        self.model = model

    def _get_callback(self, instance, value):
        if value:
            return self.model.find_one({"_id": value._id})
        return value

    def _set_callback(self, instance, value):
        if value:
            value = DBRef(self.model._get_name(), value._id)
        return value








