import json


class Symbol(object):

    def __init__(self, j):
        self.__dict__ = j

    def __repr__(self):
        return self.__dict__

    def __str__(self):
        return json.dumps(self.__dict__)
