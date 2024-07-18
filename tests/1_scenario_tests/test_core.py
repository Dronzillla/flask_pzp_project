"""
1. Anonymous user
"""


def test_core_get_index_anyonymous_user(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Not a registered user?" in response.data


def test_core_get_about_anyonymous_user(client):
    response = client.get("/about")
    assert response.status_code == 200
    assert b"Project Context" in response.data


def test_core_get_privacy_anyonymous_user(client):
    response = client.get("/privacy")
    assert response.status_code == 200
    assert b"Information We Collect" in response.data


def test_core_get_terms_anyonymous_user(client):
    response = client.get("/terms")
    assert response.status_code == 200
    assert b"Acceptance of Terms" in response.data


def test_core_get_cookies_anyonymous_user(client):
    response = client.get("/cookies")
    assert response.status_code == 200
    assert b"What are Cookies?" in response.data
