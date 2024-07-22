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
from tests.utils import login_test, create_user_test, default_user_test
import os
from dotenv import load_dotenv

load_dotenv()


"""
Application configuration for testing
"""


@pytest.fixture(scope="session")
def app():
    app = create_app(config_class="config.config.TestingConfig")
    return app


"""
Database fixtures for testing
"""


@pytest.fixture(scope="function")
def setup_database_default(app):
    # Make sure admin user is being created the same way as in app.py since we are droping database for each test
    from blueprintapp.blueprints.auth.db_operations import db_admin_user_created

    with app.app_context():
        db.create_all()
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
def setup_database_verified_user(app):
    with app.app_context():
        db.create_all()
        # Add new user who is verified
        create_user_test(is_verified=True)
        yield
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def setup_database_registered_user(app):
    with app.app_context():
        db.create_all()
        # Add new user who is not verified
        create_user_test(is_verified=False)
        yield
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def setup_database_admin_not_verified(app):
    # Make sure admin user is being created the same way as in app.py since we are droping database for each test
    from blueprintapp.blueprints.auth.db_operations import db_admin_user_created
    from blueprintapp.blueprints.auth.models import User

    with app.app_context():
        db.create_all()
        admin_username = os.getenv("ADMIN_USERNAME")
        admin_email = os.getenv("ADMIN_EMAIL")
        admin_password = os.getenv("ADMIN_PASSWORD")
        db_admin_user_created(
            username=admin_username, email=admin_email, password=admin_password
        )

        user = User.query.filter_by(email=admin_email).first()
        user.is_verified = False
        db.session.commit()

        yield
        db.session.remove()
        db.drop_all()


"""
Client fixtures for testing
"""


# 1. Anonymous user
@pytest.fixture(scope="function")
def client(app, setup_database_default):
    return app.test_client()


# 2. Registered, logged in, verified, not an admin user
@pytest.fixture(scope="function")
def client_2(app, setup_database_verified_user):
    client = app.test_client()
    # Log in the user
    username, email, password = default_user_test()
    login_test(client, email=email, password=password)
    return client


# 3. Registered, logged in, verified, an admin user
@pytest.fixture(scope="function")
def client_3(app, setup_database_default):
    client = app.test_client()
    # Get admin email and password
    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")
    # Log in admin user
    login_test(client, email=admin_email, password=admin_password)
    return client


# 4. Registered, not logged in, verified, not an admin user
@pytest.fixture(scope="function")
def client_4(app, setup_database_verified_user):
    client = app.test_client()
    return client


# 5. Registered, not logged in, verified, an admin user
"""
Already existing client fixture can be used:
1. Anonymous user
"""


# 6. Registered, not logged in, not verified, not an admin user
@pytest.fixture(scope="function")
def client_6(app, setup_database_registered_user):
    client = app.test_client()
    return client


# 7. Registered, not logged in, not verified, an admin user
@pytest.fixture(scope="function")
def client(app, setup_database_admin_not_verified):
    return app.test_client()
