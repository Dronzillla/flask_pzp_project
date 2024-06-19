from blueprintapp.app import db
from blueprintapp.blueprints.upload.models import Project, General, Ratios
from datetime import datetime


# db operations file
# Create new project
def db_create_project(name: str, code: str) -> Project:
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


def db_find_project_by_name(name: str) -> Project:
    """Checks if project exists in database based on an provided name.

    Args:
        name (str): Project name

    Returns:
        Project: 'Project' object if project exists in database, 'None' if project does not exist in database.
    """
    project = Project.query.filter_by(name=name).one_or_none()
    return project


def db_find_project_by_code(code: str) -> Project:
    """Checks if project exists in database based on an provided code.

    Args:
        name (str): Project code

    Returns:
        Project: 'Project' object if project exists in database, 'None' if project does not exist in database.
    """
    project = Project.query.filter_by(code=code).one_or_none()
    return project


def db_assign_general(
    start_date: datetime,
    reference_period: int,
    analysis_method: str,
    analysis_principle: str,
    main_sector: str,
    no_alternatives: int,
    da_analysis: bool,
    version: str,
    project_id: int,
) -> bool:
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
        return True
    except:
        return False


def db_assign_ratios(
    enis: float,
    egdv: int,
    evgn: float,
    sva: float,
    da: float,
    fgdv: int,
    fvgn: float,
    fnis: float,
    project_id: int,
) -> bool:
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

    except:
        return False
