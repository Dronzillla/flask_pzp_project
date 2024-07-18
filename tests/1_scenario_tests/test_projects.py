"""
1. Anonymous user
"""


def test_projects_get_index_anyonymous_user(client):
    response = client.get("/projects/")
    assert response.status_code == 200
    assert b"<h2>Projects</h2>" in response.data


def test_projects_get_project_not_exist_anyonymous_user(client):
    response = client.get("/projects/project/1")
    assert response.status_code == 404
    assert b"Project not found" in response.data
