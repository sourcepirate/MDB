__author__ = 'plasmashadow'

class Query(object):

    def __init__(self, Model):
        self.model = Model
        self._start_id = None
        self.cursor =