# third-party modules
from flask import Flask
from flask import render_template
from flask import request

# local modules
from models import db
from nodes import node_bp
from users import user_bp
from users import login_manager

application = Flask(__name__)

# add configurations
application.config.from_pyfile('settings.py')

# initialise database
with application.app_context():
    db.init_app(application)
    db.create_all()
    db.session.commit()

# register blueprints
application.register_blueprint(node_bp)
application.register_blueprint(user_bp)

# init login services
login_manager.init_app(application)

@application.context_processor
def inject_vars():
    return dict(client_id=application.config.get('GA_CLIENT_ID'))

@application.route('/')
def index():
    return render_template('home.html')

@application.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

if __name__ == '__main__':
    application.run(debug=True)