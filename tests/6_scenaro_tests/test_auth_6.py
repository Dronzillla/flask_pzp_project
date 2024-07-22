"""
6. Registered, not logged in, not verified, not an admin user
"""


def test_auth_post_login_user_is_registered_not_logged_not_verified_not_admin(client_6):
    # Try to log in with correct creditentials
    response = client_6.post(
        "/auth/login",
        data={"email": "test@test.com", "password": "QWERqwer1234...."},
        follow_redirects=True,
    )
    # Check that user was redirected to the same login page and not dashboard
    assert response.request.path == "/auth/login"
