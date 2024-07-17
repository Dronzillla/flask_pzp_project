def test_core_get_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Not a registered user?" in response.data


def test_core_get_about(client):
    response = client.get("/about")
    assert response.status_code == 200
    assert b"Project Context" in response.data


def test_core_get_privacy(client):
    response = client.get("/privacy")
    assert response.status_code == 200
    assert b"Information We Collect" in response.data


def test_core_get_terms(client):
    response = client.get("/terms")
    assert response.status_code == 200
    assert b"Acceptance of Terms" in response.data


def test_core_get_cookies(client):
    response = client.get("/cookies")
    assert response.status_code == 200
    assert b"What are Cookies?" in response.data
