from blueprintapp.app import db
from blueprintapp.blueprints.auth.models import User
from sqlalchemy import func


def db_read_admin_user_count() -> int:
    count = db.session.query(func.count(User.id)).filter(User.is_admin == True).scalar()
    return count


def db_read_is_verified_user_count(condition: bool) -> int:
    count = (
        db.session.query(func.count(User.id))
        .filter(User.is_verified == condition)
        .scalar()
    )
    return count
