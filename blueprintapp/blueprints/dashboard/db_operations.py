from blueprintapp.app import db
from blueprintapp.blueprints.upload.models import Project
from blueprintapp.blueprints.auth.models import User
from typing import Optional


def db_read_all_user_projects(user_id: int) -> list[Project]:
    projects = Project.query.filter_by(user_id=user_id).all()
    return projects


def db_read_project_by_id_and_user_id(id: int, user_id: int) -> Optional[Project]:
    result = Project.query.filter_by(id=id, user_id=user_id).one_or_none()
    return result


def db_delete_project(project: Project) -> None:
    db.session.delete(project)
    db.session.commit()


def db_search_all_user_projects(search_query: str, user_id: int) -> list[Project]:
    projects = Project.query.filter(
        (Project.name.ilike(f"%{search_query}%"))
        | (Project.code.ilike(f"%{search_query}%")),
        Project.user_id == user_id,
    ).all()
    return projects


def db_delete_user(user: User) -> None:
    db.session.delete(user)
    db.session.commit()


def db_read_user_by_id(id: int) -> Optional[User]:
    result = User.query.filter_by(id=id).one_or_none()
    return result
