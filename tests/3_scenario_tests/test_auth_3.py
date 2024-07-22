"""
3. Registered, logged in, verified, an admin user
"""


def test_auth_get_logout_admin_user_logged_in_and_verified(client_3):
    # Try to access logout route
    response = client_3.get("/auth/logout", follow_redirects=True)
    assert response.status_code == 200
    # Check that user was redirected to the main page
    assert response.request.path == "/"
