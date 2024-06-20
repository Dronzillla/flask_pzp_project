from blueprintapp.app import db
from blueprintapp.blueprints.upload.models import (
    Project,
    General,
    Ratios,
    Cashflow,
    Benefit,
    BenefitComponent,
    Sector,
)
from datetime import datetime

from blueprintapp.blueprints.upload.parse_project import Cashflow_tuple, Benefit_tuple
from typing import Optional


# db operations file
# Create new project
def db_create_project(name: str, code: str) -> Optional[Project]:
    """Create new project in a database.
    Each project in database has unique name and code.
    If project with provided name and code does not exist, new project gets created.
    Otherwise, no new project is created.

    Args:
        name (str): Customer first name
        code (str): Customer last name
    Returns:
        bool: 'True' - Project with provided details does not exist, 'False' - Project with provided details exist.
    """
    # If project already exists, we should not create a new one
    if db_find_project_by_name(name) is not None:
        return False
    if db_find_project_by_code(code) is not None:
        return False

    # Create new project
    project = Project(name=name, code=code)
    db.session.add(project)
    db.session.commit()
    return project


def db_find_project_by_name(name: str) -> Optional[Project]:
    """Checks if project exists in database based on an provided name.

    Args:
        name (str): Project name

    Returns:
        Project: 'Project' object if project exists in database, 'None' if project does not exist in database.
    """
    project = Project.query.filter_by(name=name).one_or_none()
    return project


def db_find_project_by_code(code: str) -> Optional[Project]:
    """Checks if project exists in database based on an provided code.

    Args:
        name (str): Project code

    Returns:
        Project: 'Project' object if project exists in database, 'None' if project does not exist in database.
    """
    project = Project.query.filter_by(code=code).one_or_none()
    return project


def db_insert_general(
    start_date: datetime,
    reference_period: int,
    analysis_method: str,
    analysis_principle: str,
    main_sector: str,
    no_alternatives: int,
    da_analysis: bool,
    version: str,
    project_id: int,
) -> Optional[General]:
    # Assign general information to a project
    general = General(
        start_date=start_date,
        reference_period=reference_period,
        analysis_method=analysis_method,
        analysis_principle=analysis_principle,
        main_sector=main_sector,
        no_alternatives=no_alternatives,
        da_analysis=da_analysis,
        version=version,
        project_id=project_id,
    )
    try:
        db.session.add(general)
        db.session.commit()
        return general
    except:
        return None


def db_insert_ratios(
    enis: float,
    egdv: int,
    evgn: float,
    sva: float,
    da: float,
    fgdv: int,
    fvgn: float,
    fnis: float,
    project_id: int,
) -> Optional[Ratios]:
    # Assign ratios to a project
    ratios = Ratios(
        enis=enis,
        egdv=egdv,
        evgn=evgn,
        sva=sva,
        da=da,
        fgdv=fgdv,
        fvgn=fvgn,
        fnis=fnis,
        project_id=project_id,
    )
    try:
        db.session.add(ratios)
        db.session.commit()
        return ratios
    except:
        return None


"""
Functions to insert cashflows
"""


def db_insert_cashflow(cashflow: Cashflow_tuple, project_id: int) -> None:
    for year, amount in cashflow["values"].items():
        record = Cashflow(
            amount=amount, year=year, category=cashflow.category, project_id=project_id
        )
        db.session.add(record)
    db.session.commit()


def db_insert_cashflows(cashflows: list[Cashflow_tuple], project_id: int) -> None:
    for cashflow in cashflows:
        db_insert_cashflow(cashflow=cashflow, project_id=project_id)


"""
Functions to insert benefits
"""


def db_insert_benefit(benefit: Benefit_tuple, benefit_id: int, project_id: int) -> None:
    for year, amount in benefit["values"].items():
        record = Benefit(
            amount=amount, year=year, benefit_id=benefit_id, project_id=project_id
        )
        db.session.add(record)
    db.session.commit()


# Return benefitcomponent or None
def db_benefit_component_exists(benefit_name: str) -> Optional[BenefitComponent]:
    benefit_component = BenefitComponent.query.filter_by(
        benefit_name=benefit_name
    ).one_or_none()
    return benefit_component


def db_insert_benefit_component(benefit_name: str) -> BenefitComponent:
    benefit_component = BenefitComponent(name=benefit_name)
    return benefit_component


def db_insert_benefits(benefits: list[Benefit_tuple], project_id: int) -> None:
    for benefit in benefits:
        # Get benefit component
        benefit_name = benefit.name
        # Check if it exists in database
        benefit_component = db_benefit_component_exists(benefit_name=benefit_name)
        # Add component if it does not exist
        if benefit_component is None:
            benefit_component = db_insert_benefit_component(benefit_name=benefit_name)
        # Retrieve benefit_component id
        benefit_id = benefit_component.id
        # Add benefit to a project
        db_insert_benefit(benefit=benefit, benefit_id=benefit_id, project_id=project_id)


"""
Functions to insert economic sectors
"""


def db_economic_sector_exists(name: str) -> Optional[Sector]:
    sector = Sector.query.filter_by(name=name).one_or_none()
    return sector


def db_insert_economic_sector(name: str) -> Sector:
    # Check if economic sector does not exist
    sector = db_economic_sector_exists(name=name)
    if sector is None:
        sector = Sector(name=name)
        db.session.add(sector)
        db.session.commit()
    return sector


def db_insert_economic_sectors(economic_sector_names: list[str]) -> list[Sector]:
    # list[Sector] for making an association
    result = []
    for name in economic_sector_names:
        sector = db_insert_economic_sector(name=name)
        result.append(sector)
    return result
