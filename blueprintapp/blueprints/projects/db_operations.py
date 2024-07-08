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


def db_read_all_projects() -> list[Project]:
    projects = Project.query.all()
    return projects


def db_read_project_by_id(id: int) -> Optional[Project]:
    result = Project.query.filter_by(id=id).one_or_none()
    return result


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


def db_search_all_projects(search_query: str) -> list[Project]:
    projects = Project.query.filter(
        (Project.name.ilike(f"%{search_query}%"))
        | (Project.code.ilike(f"%{search_query}%"))
    ).all()
    return projects
