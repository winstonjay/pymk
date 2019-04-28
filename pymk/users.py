from flask import Blueprint
from flask import render_template
from flask import request
from flask import jsonify
from flask import redirect
from flask import url_for
from flask import current_app

from flask_login import LoginManager
from flask_login import login_user
from flask_login import logout_user

from google.oauth2 import id_token
from google.auth.transport import requests

from .models import db
from .models import User
from .models import Node
from .utils import debugging

user_bp = Blueprint('users', __name__, url_prefix='/users')

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('users.login'))

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('/users/login.html')
    token = request.form.get('idtoken')
    try:
        client_id = current_app.config['GA_CLIENT_ID']
        valid_iss = ['accounts.google.com', 'https://accounts.google.com']
        # Specify the client_id of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), client_id)
        if idinfo['iss'] not in valid_iss:
            raise ValueError('Wrong issuer.')
        # ID token is valid. check user exists by Google Account ID
        # from the decoded token
        user = User.get_or_create(idinfo)
        login_user(user)
        return request.args.get('next') or '/'
    except ValueError as e:
        # Invalid token; give error
        return jsonify({'error': str(e)})

@user_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'), 301)

@debugging
@user_bp.route('/register', methods=['POST'])
def register_user():
    user = User(**request.form)
    db.session.add(user)
    db.session.commit()
    return user.json()

@debugging
@user_bp.route('/list')
def list_users():
    return jsonify([u._dict() for u in User.query.all()])