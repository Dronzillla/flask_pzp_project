from blueprintapp.app import db
from blueprintapp.blueprints.upload.models import (
    Project,
    Cashflow,
    Ratios,
    General,
    Benefit,
    BenefitComponent,
)
from typing import Optional


def db_read_all_user_projects(user_id: int) -> list[Project]:
    projects = Project.query.filter_by(user_id=user_id).all()
    return projects


def db_read_project_by_id(id: int) -> Optional[Project]:
    result = Project.query.filter_by(id=id).one_or_none()
    return result


def db_read_project_by_id_and_user_id(id: int, user_id: int) -> Optional[Project]:
    result = Project.query.filter_by(id=id, user_id=user_id).one_or_none()
    return result


def db_delete_project(project: Project) -> None:
    db.session.delete(project)
    db.session.commit()


def db_read_cashflow_by_project_id(project_id: int) -> list:
    cashflow_data = (
        db.session.query(Cashflow.year, Cashflow.amount, Cashflow.category)
        .filter_by(project_id=project_id)
        .all()
    )
    return cashflow_data


def db_read_ratios_by_project_id(project_id: int) -> Optional[Ratios]:
    ratios_data = Ratios.query.filter_by(project_id=project_id).one_or_none()
    return ratios_data


def db_read_general_by_project_id(project_id: int) -> Optional[General]:
    general_data = General.query.filter_by(project_id=project_id).one_or_none()
    return general_data


def db_read_benefits_by_project_id(
    project_id: int,
) -> list:
    benefits = (
        db.session.query(Benefit.year, Benefit.amount, BenefitComponent.name)
        .join(BenefitComponent, Benefit.benefit_id == BenefitComponent.id)
        .filter(Benefit.project_id == project_id)
        .all()
    )
    return benefits
