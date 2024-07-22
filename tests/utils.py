from blueprintapp.app import db
from blueprintapp.blueprints.auth.models import User


def login_test(client, email: str, password: str):
    return client.post(
        "/auth/login",
        data={"email": email, "password": password},
        follow_redirects=True,
    )


def default_user_test() -> tuple[str]:
    """Set up default username, email and password for testing.

    Returns:
        tuple[str]: username, email, password
    """
    username = "test"
    email = "test@test.com"
    password = "QWERqwer1234...."
    return username, email, password


def create_user_test(is_verified: bool, is_admin: bool = False) -> User:
    """Create user in database and based on arguments make user verified and admin.

    Returns:
        User:

    Args:
        is_verified (bool): 'True' - to make user verified, 'False' - to make user not verified.
        is_admin (bool, optional): _description_. Defaults to False.

    Returns:
        User: a user object
    """
    username, email, password = default_user_test()
    user = User(
        username=username, email=email, is_verified=is_verified, is_admin=is_admin
    )
    user.set_password(password=password)  # Set password using the set_password method
    db.session.add(user)
    db.session.commit()
    return User


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
