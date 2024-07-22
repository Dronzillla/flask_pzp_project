from blueprintapp.app import db
from blueprintapp.blueprints.upload.models import (
    Cashflow,
    Ratios,
    Benefit,
    BenefitComponent,
    General,
    Project,
)
from sqlalchemy import func
from collections import namedtuple
from typing import Optional
from typing import Callable

"""
Functions to get aggregate cashflows data from database
"""


def db_aggregate_cashflow_data() -> list:
    cashflow_data = (
        db.session.query(
            Cashflow.year,
            Cashflow.category,
            func.sum(Cashflow.amount).label("total_amount"),
        ).group_by(Cashflow.year, Cashflow.category)
        # When using .all method the return value is Row class (or a similar internal class) that supports both index-based and attribute-based access.
        .all()
    )
    # print(cashflow_data)
    return cashflow_data


"""
Functions to get aggregate ratios data from database
"""


def db_aggregate_ratio_averages() -> list:
    # Build custom named tuple to follow similiar logic to aggregate_cashflow_data
    RatioAverage = namedtuple("RatioAverage", ["ratio", "average"])
    # A list to hold the average values
    averages = []
    # Check if ratios table is empty, if so. Return an empty list
    ratios = Ratios.query.all()
    if len(ratios) == 0:
        return []
    # Get the list of ratio columns in db
    ratio_columns = [
        column.key
        for column in Ratios.__table__.columns
        if column.key not in ["id", "project_id"]
    ]
    # Loop through each ratio column
    for ratio in ratio_columns:
        # Create the query to calculate the average, omitting NULL and -9999.0
        average = (
            db.session.query(func.avg(getattr(Ratios, ratio)))
            .filter(
                getattr(Ratios, ratio) != None,
                getattr(Ratios, ratio) != -9999.0,
            )
            .scalar()
        )
        # Store the result in the averages list
        averages.append(RatioAverage(ratio, average))
    # print(averages)
    return averages


"""
Functions to get aggregate benefits data from database
"""


def db_aggregate_benefits_by_component_by_year() -> list:
    # Query to get the summed benefits per year and benefit component
    results = (
        db.session.query(
            Benefit.year,
            BenefitComponent.name,
            func.sum(Benefit.amount).label("total_amount"),
        )
        .join(BenefitComponent, Benefit.benefit_id == BenefitComponent.id)
        .group_by(Benefit.year, BenefitComponent.name)
        .all()
    )
    return results


"""
Functions to get general information about projects
"""


def db_unique_column_values_count(column: Callable) -> list:
    """Query database table column and calculates the count of unique values in table column.

    Args:
        column (Callable): table model and column, e.g. General.analysis_method.

    Returns:
        list: list of tuples, where each tuple represents unique column value and their corresponding count in database.
    """
    # Usage for analysis method, analysis principle, da_analysis, main_sector
    results = (
        db.session.query(column, func.count(column).label("count"))
        .group_by(column)
        .all()
    )
    return results


def db_aggregate_general_analysis_methods_count() -> list:
    # Count of unique analysis_methods in projects
    result = db_unique_column_values_count(column=General.analysis_method)
    return result


def db_aggregate_general_analysis_principle_count() -> list:
    # Count of unique analysis_principles in projects
    result = db_unique_column_values_count(column=General.analysis_principle)
    return result


def db_aggregate_general_main_sector_count() -> list:
    # Count of unique main_sector in projects
    result = db_unique_column_values_count(column=General.main_sector)
    return result


def db_column_values_average(column: Callable) -> Optional[float]:
    """Query database table column and calculates the average values in table column.

    Args:
        column (Callable): table model and column, e.g. General.no_alternatives.

    Returns:
        Optional[float]: an average value as float or 'None' if no rows are present.
    """
    average_value = db.session.query(func.avg(column).label("average")).scalar()
    return average_value


def db_aggregate_general_no_alternatives_average() -> Optional[float]:
    # Calculate an average number of alterantives in projects
    result = round(db_column_values_average(column=General.no_alternatives), 2)
    return result


def db_aggregate_general_reference_period_average() -> Optional[int]:
    # Calculate an average reference period in projects
    result = int(db_column_values_average(column=General.reference_period))
    return result


"""
Functions to get the count of projects
"""


def db_aggregate_project_count() -> int:
    """Calculate number of projects in database.

    Returns:
        int: number of uploaded projects in database.
    """
    row_count = int(db.session.query(func.count(Project.id)).scalar())
    return row_count
