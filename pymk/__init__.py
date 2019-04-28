# third-party modules
from flask import Flask
from flask import render_template
from flask import request

# local modules
from .models import db
from .nodes import node_bp
from .users import user_bp
from .users import login_manager

def create_app(**kwargs):
    app = Flask(__name__)

    # add configurations
    app.config.from_pyfile('settings.py')
    app.config.update(**kwargs)

    # initialise database
    with app.app_context():
        db.init_app(app)
        db.create_all()
        db.session.commit()

    # register blueprints
    app.register_blueprint(node_bp)
    app.register_blueprint(user_bp)

    # init login services
    login_manager.init_app(app)

    # context processors
    @app.context_processor
    def inject_vars():
        return dict(client_id=app.config.get('GA_CLIENT_ID'))

    # Auxiliary views
    @app.route('/')
    def index():
        return render_template('home.html')

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app