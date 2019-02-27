from flask import Blueprint
from flask import render_template
from flask import request

from models import db
from models import Node

node_bp = Blueprint('nodes', __name__, url_prefix='/nodes')

@node_bp.route('/link/<userid>/<hashval>')
def link_node(userid, hashval):
    context = {}
    return render_template('nodes/link.html', **context)

@node_bp.route('/share/<hashval>')
def share_node(hashval):
    context = {}
    return render_template('nodes/share.html', **context)

@node_bp.route('/register', methods=['POST'])
def register_node():
    node = Node(**request.form)
    db.session.add(node)
    db.session.commit()
    return node.json()