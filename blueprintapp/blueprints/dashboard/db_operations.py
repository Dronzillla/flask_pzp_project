from blueprintapp.app import db
from blueprintapp.blueprints.upload.models import Project
from typing import Optional


def db_read_all_user_projects(user_id: int) -> list[Project]:
    """Read all projects uploaded by user based on User.id

    Args:
        user_id (int): User.id

    Returns:
        list[Project]: a list of all 'Project' objects uploaded by user.
    """
    projects = Project.query.filter_by(user_id=user_id).all()
    return projects


def db_read_project_by_id_and_user_id(id: int, user_id: int) -> Optional[Project]:
    """Search for project by Project.id and User.id

    Args:
        id (int): Project.id
        user_id (int): User.id

    Returns:
        Optional[Project]: 'Project' object if project was found, 'None' if no project matching the filters were found.
    """
    result = Project.query.filter_by(id=id, user_id=user_id).one_or_none()
    return result


def db_delete_project(project: Project) -> None:
    """Deletes project from database

    Args:
        project (Project): 'Project' object to delete.
    """
    db.session.delete(project)
    db.session.commit()


def db_search_all_user_projects(search_query: str, user_id: int) -> list[Project]:
    """Search for all projects uploaded by user with the provided search query.

    Args:
        search_query (str): search query, usually a fraction of Project.code or Project.name
        user_id (int): User.id

    Returns:
        list[Project]: list of all 'Project' objects that matches the search query and are uploaded by 'User.id' = user_id.
    """
    projects = Project.query.filter(
        (Project.name.ilike(f"%{search_query}%"))
        | (Project.code.ilike(f"%{search_query}%")),
        Project.user_id == user_id,
    ).all()
    return projects
