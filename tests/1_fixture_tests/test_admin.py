"""
Fixture:
1. Anonymous user
"""


def test_admin_get_index_anyonymous_user(client):
    response = client.get("/admin", follow_redirects=True)
    assert response.status_code == 200
    # Check that user was redirected to login page
    assert response.request.path == "/auth/login"


def test_admin_get_user_view_anyonymous_user(client):
    response = client.get("/admin/user/", follow_redirects=True)
    assert response.status_code == 200
    # Check that user was redirected to login page
    assert response.request.path == "/auth/login"


def test_admin_get_project_view_anyonymous_user(client):
    response = client.get("/admin/project/", follow_redirects=True)
    assert response.status_code == 200
    # Check that user was redirected to login page
    assert response.request.path == "/auth/login"
