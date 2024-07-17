"""
ARCHIVE
# @pytest.fixture(scope="function")
# def app():
#     app = create_app(config_class="config.config.TestingConfig")
#     with app.app_context():
#         db.create_all()

#     yield app

#     with app.app_context():
#         db.session.remove()
#         db.drop_all()


# @pytest.fixture(scope="function")
# def client(app):
#     # Clear session between tests
#     with app.test_client() as client:
#         yield client
#         db.session.remove()


# @pytest.fixture(scope="module")
# def client(app):
#     return app.test_client()


# @pytest.fixture()
# def runner(app):
#     return app.test_cli_runner()
"""

"""
ARCHIVE
# To test with csrf tokens there is a need to insert generate_csrf
from flask_wtf.csrf import generate_csrf
csrf_token = generate_csrf()
data = (
    {
        "username": "test",
        "email": "test@test.com",
        "password": "QWERqwer1234....",
        "password2": "QWERqwer1234....",
        "csrf_token": csrf_token,
    },
)
"""
