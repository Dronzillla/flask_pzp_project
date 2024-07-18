"""
1. Anonymous user
"""


def test_upload_get_index_anyonymous_user(client):
    response = client.get("/upload", follow_redirects=True)
    assert response.status_code == 200
    # Check that user was redirected to login page
    assert response.request.path == "/auth/login"
