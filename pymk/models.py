import uuid
import hashlib
from datetime import datetime

from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

from .utils import Serializable
from .utils import unpack_kwargs

# We initialise with application in application.py
db = SQLAlchemy()


class User(db.Model, Serializable):
    '''User class defines SQLAlchemy model for user functionality within
    the site. After validation via Google, users are either made or fetched
    with get_or_create. Methods required for the 'flask_login' library are
    implemented.'''
    __tablename__ = 'user'
    user_id = db.Column(db.String(32), primary_key=True)
    ga_id = db.Column(db.String(32), unique=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    name = db.Column(db.String(100), nullable=True)
    picture = db.Column(db.String(200), nullable=True)
    active = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, default=datetime.utcnow())
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
    '''Node class defines SQLALchemy model that forms the main
    datastructure of the application. '''
    __tablename__ = 'node'
    node_id = db.Column(db.String(40), primary_key=True)
    parent_id = db.Column(db.String(40))
    user_id = db.Column(db.String(32), db.ForeignKey('user.user_id'), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    meeting = db.Column(db.DateTime, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow())

    @unpack_kwargs
    def __init__(self, **kwargs):
        parent = Node.query.filter_by(node_id=kwargs['parent_id']).first()
        if parent is None:
            raise ValueError('unknown parent node')
        if parent.user.user_id == kwargs['user_id']:
            raise ValueError('self-referential user connection')
        self.node_id = self.generate_id(**kwargs)
        self.meeting = datetime.strptime(kwargs['meeting'], '%Y-%m-%d')
        super(Node, self).__init__(**kwargs)

    def generate_id(self, **kwargs):
        'return sha1 hexdigest of joined args'
        z = ''.join([kwargs['parent_id'], kwargs['user_id']]).encode('utf-8')
        return hashlib.sha1(z).hexdigest()
