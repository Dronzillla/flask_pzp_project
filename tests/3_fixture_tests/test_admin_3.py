"""
Fixture:
3. Registered, logged in, verified, an admin user
"""


def test_admin_get_index_admin_user_logged_in_and_verified(client_3):
    response = client_3.get("/admin", follow_redirects=True)
    assert response.status_code == 200
    # Check that user was able to access admin page
    assert response.request.path == "/admin/"
    # Check for unique text in admin page
    assert b"Admin Dashboard" in response.data


def test_admin_get_admin_user_view_user_logged_in_and_verified(client_3):
    response = client_3.get("/admin/user", follow_redirects=True)
    assert response.status_code == 200
    # Check that user was able to access user models page
    assert response.request.path == "/admin/user/"
    # Check for unique text in model view page
    assert b"Username" in response.data


def test_admin_get_project_view_admin_user_logged_in_and_verified(client_3):
    response = client_3.get("/admin/project", follow_redirects=True)
    assert response.status_code == 200
    # Check that user was able to access project models page
    assert response.request.path == "/admin/project/"
    # Check for unique text in model view page
    assert b"Code" in response.data
