"""
Fixture:
2. Registered, logged in, verified, not an admin user
"""


def test_dashboard_get_index_user_logged_in_and_verified(client_2):
    response = client_2.get("/dashboard/")
    assert response.status_code == 200
    # Check that user was redirected to login page
    assert response.request.path == "/dashboard/"
    # Check for unique information from dashboard
    assert b"Uploaded Projects" in response.data
