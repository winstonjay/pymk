from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import jsonify
from flask import abort

from flask_login import login_required
from flask_login import current_user

from sqlalchemy.exc import IntegrityError

from .models import db
from .models import Node
from .utils import debugging

node_bp = Blueprint('nodes', __name__, url_prefix='/nodes')

@login_required
@node_bp.route('/link/<parent_id>')
def link_node(parent_id):
    parent = Node.query.filter_by(node_id=parent_id).first()
    if parent is None:
        abort(404)
    if parent.user.user_id == current_user.user_id:
        return render_template('nodes/share.html', parent=parent)
    return render_template('nodes/link.html', parent=parent)

@login_required
@node_bp.route('/register', methods=['POST'])
def register_node():
    try:
        node = Node(**request.form)
        db.session.add(node)
        db.session.commit()
        return node.json()
    except (ValueError, IntegrityError) as e:
        return jsonify({'error': str(e)})

@debugging
@node_bp.route('/list')
def list_nodes():
    return jsonify([u._dict() for u in Node.query.all()])