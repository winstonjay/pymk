import uuid
import hashlib
import datetime

from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

# db initialised with application in application.py
db = SQLAlchemy()

class Serializable(object):
    'Helper class for serializing SQLAlchemy objects'

    def dict(self):
        cols = self.__table__.columns
        return {c.name: getattr(self, c.name) for c in cols}

    def json(self):
        return jsonify(self.dict())


# kwargs from request.form seem to be unpacking single args as
# lists. Check if this is the case and return the args unpacked.
def unpack_kwargs(func):
    def wrapper(*args, **kwargs):
        _kwargs = dict((k, v[0] if isinstance(v, (list,)) else v)
                        for k, v in kwargs.items())
        func(*args, **_kwargs)
    return wrapper


class User(db.Model, Serializable):
    __tablename__ = 'user'
    user_id = db.Column(db.String(32), primary_key=True)
    ga_id = db.Column(db.String(32), unique=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    picture = db.Column(db.String(200), nullable=True)
    active = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    nodes = db.relationship('Node', backref='user', lazy=True)

    @unpack_kwargs
    def __init__(self, **kwargs):
        self.user_id = uuid.uuid1().hex
        super(User, self).__init__(**kwargs)

    @classmethod
    def get_or_create(cls, idinfo):
        user = User.query.filter_by(ga_id=idinfo['sub']).first()
        if not user:
            user = User(name=idinfo.get('name'),
                        email=idinfo.get('email'),
                        ga_id=idinfo.get('sub'),
                        picture=idinfo.get('picture'),
                        active=True)
            db.session.add(user)
            db.session.commit()
        return user

    @classmethod
    def get(cls, user_id):
        return User.query.filter_by(user_id=user_id).first()

    #### flask_login required methods

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.user_id


class Node(db.Model, Serializable):
    __tablename__ = 'node'
    node_id = db.Column(db.String(40), primary_key=True)
    parent_id = db.Column(db.String(40))
    user_id = db.Column(db.String(32), db.ForeignKey('user.user_id'), nullable=False)
    content = db.Column(db.String(2048), nullable=False)
    meeting = db.Column(db.DateTime, nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    db.ForeignKeyConstraint(['invoice_id', 'ref_num'], ['invoice.invoice_id', 'invoice.ref_num'])


    @unpack_kwargs
    def __init__(self, **kwargs):
        self.node_id = sha1hash(kwargs['parent_id'], kwargs['user_id'])
        kwargs['meeting'] = datetime.datetime(*list(map(int, kwargs['meeting'].split('-'))))
        super(Node, self).__init__(**kwargs)


def sha1hash(self, *args):
    'return sha1 hexdigest of joined args'
    return hashlib.sha1(cat(args).encode('utf-8')).hexdigest()

cat = ''.join
