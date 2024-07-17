import pytest
from blueprintapp.app import create_app, db


@pytest.fixture(scope="session")
def app():
    app = create_app(config_class="config.config.TestingConfig")
    return app


@pytest.fixture(scope="function")
def setup_database(app):
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def client(app, setup_database):
    return app.test_client()
