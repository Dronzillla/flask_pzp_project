"""
2. Registered, logged in, verified, not an admin user
"""


def test_admin_get_index_user_logged_in_and_verified(client_2):
    # Try to access admin page
    response = client_2.get("/admin", follow_redirects=True)
    assert response.status_code == 200
    # Check that user was redirected to the dashboard page
    assert response.request.path == "/dashboard/"


def test_admin_get_user_view_user_logged_in_and_verified(client_2):
    response = client_2.get("/admin/user/", follow_redirects=True)
    assert response.status_code == 200
    # Check that user was redirected to the dashboard page
    assert response.request.path == "/dashboard/"


def test_admin_get_project_view_user_logged_in_and_verified(client_2):
    response = client_2.get("/admin/project/", follow_redirects=True)
    assert response.status_code == 200
    # Check that user was redirected to the dashboard page
    assert response.request.path == "/dashboard/"


# def test_admin_get_index_user_logged_in(client_2, app):
#     with client_2:
#         with app.app_context():
#             user = User.query.filter_by(email="test@test.com").first()
#             login_user(user)

#         # Try to access admin page (no separate with block needed)
#         response = client_2.get("/admin", follow_redirects=True)

#     assert response.status_code == 200
#     # Check that user was redirected to the dashboard page
#     assert response.request.path == "/dashboard/"


"""
Logged in verified admin user tries to access admin routes
"""
