from flask import Blueprint
from flask import render_template
from flask import request

from flask_login import login_required

from models import db
from models import Node

node_bp = Blueprint('nodes', __name__, url_prefix='/nodes')

@node_bp.route('/link/<parent_id>')
@login_required
def link_node(parent_id):
    # get the parent node
    parent = Node.query.filter_by(node_id=parent_id).first()
    if parent is None:
        return '404'
    # Requirements
    # - parent node must exist
    # - parent user can't be current user
    return render_template('nodes/link.html', **dict(parent=parent))

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