from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from db_map import DB_COLUMN_MAP
from dotenv import load_dotenv
import os

load_dotenv()
db = SQLAlchemy()
login = LoginManager()
mail = Mail()
db_column_map = DB_COLUMN_MAP


def create_app(config_class="config.config.DevelopmentConfig"):
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(config_class)

    # Set up db
    db.init_app(app)

    # Set up LoginManager
    login.init_app(app)
    login.login_view = "auth.login"

    # Set up Mail
    mail.init_app(app)

    # Import and register all blueprints
    from blueprintapp.blueprints.core.routes import core
    from blueprintapp.blueprints.upload.routes import upload
    from blueprintapp.blueprints.people.routes import people
    from blueprintapp.blueprints.auth.routes import auth
    from blueprintapp.blueprints.dashboard.routes import dashboard
    from blueprintapp.blueprints.projects.routes import projects
    from blueprintapp.blueprints.admin_bp.routes import admin_bp, init_admin

    # Register blueprints
    app.register_blueprint(core, url_prefix="/")
    app.register_blueprint(upload, url_prefix="/upload")
    app.register_blueprint(people, url_prefix="/people")
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(dashboard, url_prefix="/dashboard")
    app.register_blueprint(projects, url_prefix="/projects")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # Initialize Flask-Admin with the app context
    init_admin(app)

    # Create admin user if first admin user does not exist
    from blueprintapp.blueprints.auth.db_operations import db_admin_user_created

    with app.app_context():
        db.create_all()
        admin_username = os.getenv("ADMIN_USERNAME")
        admin_email = os.getenv("ADMIN_EMAIL")
        admin_password = os.getenv("ADMIN_PASSWORD")
        db_admin_user_created(
            username=admin_username, email=admin_email, password=admin_password
        )

    # SQL does not support alter tables. Might include: render_as_batch=True
    migrate = Migrate(app, db)
    # To create db go to blueprintapp folder where app.py is
    # flask db init
    # flask db migrate
    # flask db upgrade

    return app
