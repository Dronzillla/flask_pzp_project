"""
2. Registered, logged in, verified, not an admin user
"""


def test_upload_get_index_user_logged_in_and_verified(client_2):
    response = client_2.get("/upload/")
    assert response.status_code == 200
    # Check that user was redirected to login page
    assert response.request.path == "/upload/"
    # Check for unique information from dashboard
    assert b"<h1>Upload</h1>" in response.data
