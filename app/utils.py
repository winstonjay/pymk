
from flask import jsonify

class Serializable(object):
    'Helper class for serializing SQLAlchemy objects'

    def dict(self):
        cols = self.__table__.columns
        return {c.name: getattr(self, c.name) for c in cols}

    def json(self):
        return jsonify(self.dict())

def unpack_kwargs(func):
    def wrapper(*args, **kwargs):
        _kwargs = dict((k, _unpack_arg(v))
                    for k, v in kwargs.items())
        func(*args, **_kwargs)
    return wrapper

def _unpack_arg(arg):
    try:
        return arg[0]
    except:
        return arg