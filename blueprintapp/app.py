from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


db = SQLAlchemy()
login = LoginManager()


def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config["SECRET_KEY"] = "your_secret_key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./app.db"
    db.init_app(app)

    # Set up the LoginManager
    login.init_app(app)
    login.login_view = "auth.login"

    # import and register all blueprints
    # todos is not a file, it is blueprint
    from blueprintapp.blueprints.core.routes import core
    from blueprintapp.blueprints.upload.routes import upload
    from blueprintapp.blueprints.people.routes import people
    from blueprintapp.blueprints.auth.routes import auth

    # in order to go to index we need to go to -> todos/
    # to create an account /todos/create
    app.register_blueprint(core, url_prefix="/")
    app.register_blueprint(upload, url_prefix="/upload")
    app.register_blueprint(people, url_prefix="/people")
    app.register_blueprint(auth, url_prefix="/auth")

    migrate = Migrate(app, db)
    # To create db go to blueprintapp folder where app.py is
    # flask db init
    # flask db migrate
    # flask db upgrade

    return app
