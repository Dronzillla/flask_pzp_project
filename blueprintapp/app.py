from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()


def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config["SECRET_KEY"] = "your_secret_key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./app.db"
    db.init_app(app)

    # import and register all blueprints
    # todos is not a file, it is blueprint
    from blueprintapp.blueprints.core.routes import core
    from blueprintapp.blueprints.upload.routes import upload
    from blueprintapp.blueprints.people.routes import people

    # in order to go to index we need to go to -> todos/
    # to create an account /todos/create
    app.register_blueprint(core, url_prefix="/")
    app.register_blueprint(upload, url_prefix="/upload")
    app.register_blueprint(people, url_prefix="/people")

    migrate = Migrate(app, db)
    # To create db go to blueprintapp folder where app.py is
    # flask db init
    # flask db migrate
    # flask db upgrade

    return app
