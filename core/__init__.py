import os
from flask import Flask
from config import app_config
from flask_migrate import Migrate
from core.models.todo import db
from core.task import views
from flask_login import LoginManager
from datetime import timedelta
from flask_jwt_extended import JWTManager


app = Flask(__name__)
login = LoginManager()


def create_app():
    # create and configure the app
    app.config.from_object(app_config[os.environ.get("APP_SETTINGS")])
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    db.init_app(app)
    login.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    login.login_view = "auth.login"

    from core import routes

    # blueprint for non-authentication parts, auth routes and home routes of the app
    from .task import task as task_blueprint
    from .home import home as home_blueprint
    from .auth import auth as auth_blueprint

    app.register_blueprint(task_blueprint, url_prefix="/task")
    app.register_blueprint(home_blueprint, url_prefix="/home")
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    return app
