from flask import Blueprint
from flask import render_template
from flask import request
from flask import jsonify

from models import db
from models import User

user_bp = Blueprint('users', __name__, url_prefix='/users')

@user_bp.route('/register', methods=['POST'])
def register_user():
    user = User(**request.form)
    print(user.dict())
    db.session.add(user)
    db.session.commit()
    return user.json()

@user_bp.route('/list')
def list_users():
    return jsonify([u.dict() for u in User.query.all()])