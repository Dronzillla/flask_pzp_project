from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from db_map import DB_COLUMN_MAP

db = SQLAlchemy()
login = LoginManager()
db_column_map = DB_COLUMN_MAP


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
    from blueprintapp.blueprints.dashboard.routes import dashboard
    from blueprintapp.blueprints.projects.routes import projects
    from blueprintapp.blueprints.admin_bp.routes import admin_bp, init_admin

    # in order to go to index we need to go to -> todos/
    # to create an account /todos/create
    app.register_blueprint(core, url_prefix="/")
    app.register_blueprint(upload, url_prefix="/upload")
    app.register_blueprint(people, url_prefix="/people")
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(dashboard, url_prefix="/dashboard")
    app.register_blueprint(projects, url_prefix="/projects")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # Initialize Flask-Admin with the app context
    init_admin(app)

    # SQL does not support alter tables. Might include: render_as_batch=True
    migrate = Migrate(app, db)
    # To create db go to blueprintapp folder where app.py is
    # flask db init
    # flask db migrate
    # flask db upgrade

    return app
