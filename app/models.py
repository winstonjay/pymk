import uuid
import hashlib

from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

from utils import unpack_kwargs
from utils import Serializable

# db initialised with application in application.py
db = SQLAlchemy()


class User(db.Model, Serializable):
    __tablename__ = 'user'
    user_id = db.Column(db.String(32), primary_key=True)
    username = db.Column(db.String(64), primary_key=True, unique=True)
    nodes = db.relationship('Node', backref='user', lazy=True)

    @unpack_kwargs
    def __init__(self, **kwargs):
        self.user_id = uuid.uuid1().hex
        super(User, self).__init__(**kwargs)


class Node(db.Model, Serializable):
    __tablename__ = 'node'
    node_id = db.Column(db.String(40), primary_key=True)
    parent_id = db.Column(db.String(40))
    user_id = db.Column(db.String(32), db.ForeignKey('user.user_id'), nullable=False)
    content = db.Column(db.String(2048), nullable=False)
    db.ForeignKeyConstraint(['invoice_id', 'ref_num'], ['invoice.invoice_id', 'invoice.ref_num'])
    # meeting = db.Column(db.DateTime, nullable=False)
    # created = db.Column(db.DateTime)

    @unpack_kwargs
    def __init__(self, **kwargs):
        self.node_id = sha1hash(kwargs['parent_id'],
                                kwargs['user_id'])
        super(Node, self).__init__(**kwargs)


def sha1hash(self, *args):
    'return sha1 hexdigest of joined args'
    return hashlib.sha1(cat(args).encode('utf-8')).hexdigest()

cat = ''.join
