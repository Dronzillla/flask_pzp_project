from blueprintapp.app import db
from blueprintapp.blueprints.upload.models import (
    Cashflow,
    Ratios,
    Benefit,
    BenefitComponent,
)
from sqlalchemy import func
from collections import namedtuple


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


def db_aggregate_ratio_averages() -> list:
    # Build custom named tuple to follow similiar logic to aggregate_cashflow_data
    RatioAverage = namedtuple("RatioAverage", ["ratio", "average"])
    # A list to hold the average values
    averages = []
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
