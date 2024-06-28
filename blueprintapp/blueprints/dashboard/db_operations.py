from blueprintapp.app import db
from blueprintapp.blueprints.upload.models import Project
from typing import Optional


def db_read_all_user_projects(user_id: int) -> list[Project]:
    projects = Project.query.filter_by(user_id=user_id).all()
    return projects


def db_read_project_by_id(id: int, user_id: int) -> Optional[Project]:
    return Project.query.filter_by(id=id, user_id=user_id).one_or_none()


def db_delete_project(project: Project) -> None:
    db.session.delete(project)
    db.session.commit()
