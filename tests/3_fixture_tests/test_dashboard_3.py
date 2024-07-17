"""
Fixture:
3. Registered, logged in, verified, an admin user
"""


def test_dashboard_get_index_admin_user_logged_in_and_verified(client_3):
    response = client_3.get("/dashboard/")
    assert response.status_code == 200
    # Check that user was redirected to login page
    assert response.request.path == "/dashboard/"
    # Check for unique information from dashboard
    print(response.data)
    assert b"Uploaded Projects" in response.data
