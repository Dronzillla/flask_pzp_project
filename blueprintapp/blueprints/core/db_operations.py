from blueprintapp.app import db
from blueprintapp.blueprints.upload.models import Cashflow
from sqlalchemy import func


def db_aggregate_cashflow_data() -> list:
    cashflow_data = (
        db.session.query(
            Cashflow.year,
            Cashflow.category,
            func.sum(Cashflow.amount).label("total_amount"),
        )
        .group_by(Cashflow.year, Cashflow.category)
        .all()
    )
    return cashflow_data
