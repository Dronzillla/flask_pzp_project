"""
4. Registered, not logged in, verified, not an admin user
"""


def test_auth_post_login_user_is_registered_not_logged_is_verified_not_admin(client_4):
    # Try to log in with correct credidentials
    response = client_4.post(
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
