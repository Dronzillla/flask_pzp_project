def test_auth_get_register(client):
    response = client.get("/auth/register")
    assert response.status_code == 200
    # Check for unique text in page
    assert b"Already registered?" in response.data


def test_auth_get_login(client):
    response = client.get("/auth/login")
    assert response.status_code == 200
    # Check for unique text in page
    assert b"Don't have an account yet?" in response.data
    assert b"Forgot your password?" in response.data


def test_auth_get_reset_password_request(client):
    response = client.get("/auth/reset_password_request")
    assert response.status_code == 200
    # Check for unique text in page
    assert b"Request Password Reset" in response.data


def test_auth_get_logout_user_not_logged_in(client):
    response = client.get("/auth/logout", follow_redirects=True)
    # Check that user was redirected to login page
    assert response.request.path == "/auth/login"


def test_auth_post_register_correct_user_data(client):
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


def test_auth_post_register_different_user_passwords(client):
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


def test_auth_post_login_user_is_verified(client):
    # Register user
    client.post(
        "/auth/register",
        data={
            "username": "test",
            "email": "test@test.com",
            "password": "QWERqwer1234....",
            "password2": "QWERqwer1234....",
        },
    )
    # Make user verified
    from blueprintapp.blueprints.auth.models import User
    from blueprintapp.app import db

    with client.application.app_context():
        user = User.query.filter_by(email="test@test.com").first()
        user.is_verified = True
        db.session.commit()
    # Try to log in
    response = client.post(
        "/auth/login",
        data={"email": "test@test.com", "password": "QWERqwer1234...."},
        follow_redirects=True,
    )
    # Check that response include logged in user data
    assert b"Logged in as: test" in response.data
    # Check that there was one redirect response
    assert len(response.history) == 1
    # Check response status code
    assert response.status_code == 200
    # Check that the second request was to dasboard page
    assert response.request.path == "/dashboard/"


def test_auth_post_login_user_not_verified(client):
    # Register user
    client.post(
        "/auth/register",
        data={
            "username": "test1",
            "email": "test1@test.com",
            "password": "QWERqwer1234....",
            "password2": "QWERqwer1234....",
        },
    )
    # Try to log in
    response = client.post(
        "/auth/login",
        data={"email": "test1@test.com", "password": "QWERqwer1234...."},
        follow_redirects=True,
    )
    # Check that user was redirected to the same login page and not dashboard
    assert response.request.path == "/auth/login"
