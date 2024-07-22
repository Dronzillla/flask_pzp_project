"""
1. Anonymous user
"""


def test_auth_get_register_anyonymous_user(client):
    response = client.get("/auth/register")
    assert response.status_code == 200
    # Check for unique text in page
    assert b"Already registered?" in response.data


def test_auth_get_login_anyonymous_user(client):
    response = client.get("/auth/login")
    assert response.status_code == 200
    # Check for unique text in page
    assert b"Don't have an account yet?" in response.data
    assert b"Forgot your password?" in response.data


def test_auth_get_reset_password_request_anyonymous_user(client):
    response = client.get("/auth/reset_password_request")
    assert response.status_code == 200
    # Check for unique text in page
    assert b"Request Password Reset" in response.data


def test_auth_get_logout_user_anyonymous_user(client):
    response = client.get("/auth/logout", follow_redirects=True)
    # Check that user was redirected to login page
    assert response.request.path == "/auth/login"


def test_auth_post_register_anyonymous_user_correct_data(client):
    response = client.post(
        "/auth/register",
        data={
            "username": "test",
            "email": "test@test.com",
            "password": "QWERqwer1234....",
            "password2": "QWERqwer1234....",
        },
        follow_redirects=True,
    )
    # Check response status code
    assert response.status_code == 200
    # Check flash message
    assert (
        b"Congratulations, you are now a registered user. Note that an admin user still has to verify your account."
        in response.data
    )
    # Check that there was one redirect response
    assert len(response.history) == 1
    # Check that the second request was to login page
    assert response.request.path == "/auth/login"
    # Check that user was added to a database
    from blueprintapp.blueprints.auth.models import User

    with client.application.app_context():
        user = User.query.filter_by(email="test@test.com").first()
        assert user is not None
        assert user.username == "test"


def test_auth_post_register_anyonymous_user_different_passwords(client):
    response = client.post(
        "/auth/register",
        data={
            "username": "test",
            "email": "test@test.com",
            "password": "QWERqwer1234....",
            "password2": "WERqwer1234....",
        },
        follow_redirects=True,
    )

    # Check response status code
    assert response.status_code == 200
    # Check if there is error code that password must be equal.
    assert b"Field must be equal to password." in response.data
    # Check that the second request was to login page
    assert response.request.path == "/auth/register"
