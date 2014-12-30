from config import config
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap
from flask.ext.login import LoginManager



db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
def create_app(config_name):
    app = Flask(__name__)
    db.init_app(app)
    bootstrap.init_app(app)
    app.config.from_object(config[config_name])
    login_manager.init_app(app)

    from main import main as bp_main
    app.register_blueprint(bp_main)
    from auth import auth as bp_auth
    app.register_blueprint(bp_auth)

    @app.template_filter('reverse')
    def dates(s):
        return s.strftime('%Y-%m-%d %H:%M')
    app.jinja_env.filters['date'] = dates
    return app
