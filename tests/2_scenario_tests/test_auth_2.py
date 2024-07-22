"""
2. Registered, logged in, verified, not an admin user
"""


def test_auth_get_logout_user_logged_in_and_verified(client_2):
    # Try to access logout route
    response = client_2.get("/auth/logout", follow_redirects=True)
    assert response.status_code == 200
    # Check that user was redirected to the main page
    assert response.request.path == "/"
