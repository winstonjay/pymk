from flask import abort
from flask import current_app


class Serializable(object):
    'Helper class for serializing SQLAlchemy objects'

    def _dict(self):
        cols = self.__table__.columns
        return {c.name: getattr(self, c.name) for c in cols}

    def json(self):
        return jsonify(self._dict())


# kwargs from request.form seem to be unpacking single args as
# lists. Check if this is the case and return the args unpacked.
def unpack_kwargs(func):
    def wrapper(*args, **kwargs):
        _kwargs = dict((k, v[0] if isinstance(v, (list,)) else v)
                        for k, v in kwargs.items())
        func(*args, **_kwargs)
    return wrapper

def debugging(func):
    def wrapper(*args, **kwargs):
        if not current_app.config.get('DEBUG'):
            abort(404)
        return func(*args, **kwargs)
    return wrapper


