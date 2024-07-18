"""
Scenarios:
1. Anonymous user
2. Registered, logged in, verified, not an admin user
3. Registered, logged in, verified, an admin user
4. Registered, not logged in, verified, not an admin user
5. Registered, not logged in, verified, an admin user
6. Registered, not logged in, not verified, not an admin user
7. Registered, not logged in, not verified, an admin user
"""

import pytest
from blueprintapp.app import create_app, db
from blueprintapp.blueprints.auth.models import User
from tests.utils import login
import os
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session")
def app():
    app = create_app(config_class="config.config.TestingConfig")
    return app


"""
Scenario:
1. Anonymous user
"""


@pytest.fixture(scope="function")
def setup_database(app):
    # Create admin user if first admin user does not exist
    from blueprintapp.blueprints.auth.db_operations import db_admin_user_created

    with app.app_context():
        db.create_all()
        # Make sure admin user is being created the same as in app.py since we are droping database for each test
        admin_username = os.getenv("ADMIN_USERNAME")
        admin_email = os.getenv("ADMIN_EMAIL")
        admin_password = os.getenv("ADMIN_PASSWORD")
        db_admin_user_created(
            username=admin_username, email=admin_email, password=admin_password
        )

        yield
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def client(app, setup_database):
    return app.test_client()


"""
Scenario:
2. Registered, logged in, verified, not an admin user
"""


@pytest.fixture(scope="function")
def setup_database_2(app):
    with app.app_context():
        db.create_all()

        # Add new user with hashed password
        user = User(
            username="test",
            email="test@test.com",
            is_verified=True,
        )
        user.set_password(
            "QWERqwer1234...."
        )  # Set password using the set_password method
        db.session.add(user)
        db.session.commit()

        yield
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def client_2(app, setup_database_2):
    client = app.test_client()
    # Log in the user
    login(client, email="test@test.com", password="QWERqwer1234....")
    return client


"""
Scenario:
3. Registered, logged in, verified, an admin user
"""


@pytest.fixture(scope="function")
def client_3(app, setup_database):
    # app.config["SERVER_NAME"] = "127.0.0.1:5000"
    client = app.test_client()

    # Get admin email and password
    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")

    # Log in admin user
    login(client, email=admin_email, password=admin_password)
    return client
