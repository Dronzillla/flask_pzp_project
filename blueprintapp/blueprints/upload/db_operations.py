from blueprintapp.app import db
from blueprintapp.blueprints.upload.models import (
    Project,
    General,
    Ratios,
    Cashflow,
    Benefit,
    BenefitComponent,
    Sector,
    HarmComponent,
    Harm,
    project_sector,
)
from datetime import datetime

from blueprintapp.blueprints.upload.parse_project import (
    Benefit_tuple,
    Cashflow_tuple,
    General_tuple,
    Harm_tuple,
    Project_tuple,
    Ratios_tuple,
)
from typing import Optional


# db operations file
# Create new project
def db_create_project(project_tuple: Project_tuple) -> Optional[Project]:
    """Create new project in a database.
    Each project in database has unique name and code.
    If project with provided project.name and project.code does not exist, new project gets created.
    Otherwise, no new project is created.

    Args:
        project (Project_tuple): object, which has data for project 'name' and 'code' attributes.
    Returns:
        Project: - 'Project' object if new project was successfully crreated, 'False' - if project.code or project.name already exists in database.
    """
    # If project already exists, we should not create a new one
    if db_find_project_by_name(name=project_tuple.name) is not None:
        return False
    if db_find_project_by_code(code=project_tuple.code) is not None:
        return False

    # Create new project
    project = Project(name=project_tuple.name, code=project_tuple.code)
    db.session.add(project)
    db.session.commit()
    return project


def db_assign_project_information(
    project: Project,
    general: General_tuple,
    ratios: Ratios_tuple,
    cashflows: list[Cashflow_tuple],
    benefits: list[Benefit_tuple],
    harms: list[Harm_tuple],
    economic_sector_names: list[str],
) -> None:
    """Assigns project information extracted from uploaded excel spreadsheet to database tables.

    Args:
        project (Project): project database model
        general (General_tuple): tuple with multiple attributes for general project information.
        ratios (Ratios_tuple): tuple with multiple attributes for different ratios of a project.
        cashflows (list[Cashflow_tuple]): list of tuples for time series data for cashflows: capex, opex, etc of a project.
        benefits (list[Benefit_tuple]): list of tuples for time series data for specific benefit component and their respective cahsflows for a project.
        harms (list[Harm_tuple]): list of tuples for time series data for specific harm component and their respective cahsflows for a project.
        economic_sector_names (list[str]): list of economic sector names assigned to a project.
    """

    try:
        # Assign general information
        db_insert_general(general, project_id=project.id)
        # Assign ratios
        db_insert_ratios(ratios=ratios, project_id=project.id)
        # Assign cashflows
        db_insert_cashflows(cashflows=cashflows, project_id=project.id)
        # Assign benefits
        db_insert_benefits(benefits=benefits, project_id=project.id)
        # Assign harms
        db_insert_harms(harms=harms, project_id=project.id)
        # Insert sectors and assign to project
        db_insert_economic_sectors(
            economic_sector_names=economic_sector_names, project=project
        )
        # TODO Assign sectors to project
        # for economic_sector in economic_sectors:
        #     project.sectors.append(economic_sector)
        #     db.session.commit()

    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")


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


def db_project_exists(project_tuple: Project_tuple) -> bool:
    """Checks if project exists in database based on

    Args:
        project_tuple (Project_tuple): Object with attributes 'name' and 'code'.

    Returns:
        bool: 'True' if project with provided 'name' or 'code' does not exist in database, 'False' if project with provided 'name' or 'code' exists in database.
    """
    if (
        db_find_project_by_name(name=project_tuple.name) is None
        and db_find_project_by_code(code=project_tuple.code) is None
    ):
        return False
    return True


def db_insert_general(
    general: General_tuple,
    project_id: int,
) -> Optional[General]:
    # Assign general information to a project
    general = General(
        start_date=general.start_date,
        reference_period=general.reference_period,
        analysis_method=general.analysis_method,
        analysis_principle=general.analysis_principle,
        main_sector=general.main_sector,
        no_alternatives=general.no_alternatives,
        da_analysis=general.da_analysis,
        version=general.version,
        project_id=project_id,
    )
    try:
        db.session.add(general)
        db.session.commit()
        return general
    except:
        return None


def db_insert_ratios(
    ratios: Ratios_tuple,
    project_id: int,
) -> Optional[Ratios]:
    # Assign ratios to a project
    ratios = Ratios(
        enis=ratios.enis,
        egdv=ratios.egdv,
        evgn=ratios.evgn,
        sva=ratios.sva,
        da=ratios.da,
        fgdv=ratios.fgdv,
        fvgn=ratios.fvgn,
        fnis=ratios.fnis,
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
    for year, amount in cashflow.values.items():
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
    for year, amount in benefit.values.items():
        record = Benefit(
            amount=amount, year=year, benefit_id=benefit_id, project_id=project_id
        )
        db.session.add(record)
        db.session.commit()


# Return benefitcomponent or None
def db_benefit_component_exists(name: str) -> Optional[BenefitComponent]:
    benefit_component = BenefitComponent.query.filter_by(name=name).one_or_none()
    return benefit_component


def db_insert_benefit_component(name: str) -> BenefitComponent:
    benefit_component = BenefitComponent(name=name)
    db.session.add(benefit_component)
    db.session.commit()
    return benefit_component


def db_insert_benefits(benefits: list[Benefit_tuple], project_id: int) -> None:
    for benefit in benefits:
        # Get benefit component
        name = benefit.name
        # Check if it exists in database
        benefit_component = db_benefit_component_exists(name=name)
        # Add component if it does not exist
        if benefit_component is None:
            benefit_component = db_insert_benefit_component(name=name)
        # Retrieve benefit_component id
        benefit_id = benefit_component.id
        # Add benefit to a project
        db_insert_benefit(benefit=benefit, benefit_id=benefit_id, project_id=project_id)


"""
Functions to insert harms
"""


def db_insert_harm(harm: Harm_tuple, harm_id: int, project_id: int) -> None:
    for year, amount in harm.values.items():
        record = Harm(amount=amount, year=year, harm_id=harm_id, project_id=project_id)
        db.session.add(record)
        db.session.commit()


# Return harmcomponent or None
def db_harm_component_exists(name: str) -> Optional[HarmComponent]:
    harm_component = HarmComponent.query.filter_by(name=name).one_or_none()
    return harm_component


def db_insert_harm_component(name: str) -> HarmComponent:
    harm_component = HarmComponent(name=name)
    db.session.add(harm_component)
    db.session.commit()
    return harm_component


def db_insert_harms(harms: list[Harm_tuple], project_id: int) -> None:
    for harm in harms:
        # Get harm component
        name = harm.name
        # Check if it exists in database
        harm_component = db_harm_component_exists(name=name)
        # Add component if it does not exist
        if harm_component is None:
            harm_component = db_insert_harm_component(name=name)
        # Retrieve harm_component id
        harm_id = harm_component.id
        # Add harm to a project
        db_insert_harm(harm=harm, harm_id=harm_id, project_id=project_id)


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


def db_insert_economic_sectors(
    economic_sector_names: list[str], project: Project
) -> None:
    # list[Sector] for making an association
    # result = []
    for name in economic_sector_names:
        # Get new sector or create new sector if it does not exist
        sector = db_insert_economic_sector(name=name)
        # Append to project_sector association table
        project.sectors.append(sector)
        db.session.commit()

        # result.append(sector)
    # return result


# def db_assign_economic_sectors(
#     project: Project, economic_sectors: list[Sector]
# ) -> None:
#     for economic_sector in economic_sectors:
#         project.sectors.append(economic_sector)
#         db.session.commit()
