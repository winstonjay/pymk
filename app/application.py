from flask import Flask
from flask import render_template

from models import db

from nodes import node_bp
from users import user_bp

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

@application.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    application.run(debug=True)