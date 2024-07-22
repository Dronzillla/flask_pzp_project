from blueprintapp.app import db
from blueprintapp.blueprints.auth.models import User
from sqlalchemy import func


def db_read_admin_user_count() -> int:
    """Calculates how many admin users are in database.

    Returns:
        int: number of admin users.
    """
    count = db.session.query(func.count(User.id)).filter(User.is_admin == True).scalar()
    return count


def db_read_is_verified_user_count(condition: bool) -> int:
    """Calulates how many users are verified or unverified.

    Args:
        condition (bool): 'True' for verified users count, 'False' for unverified users count.

    Returns:
        int: Returns the count of verified or unverified users.
    """
    count = (
        db.session.query(func.count(User.id))
        .filter(User.is_verified == condition)
        .scalar()
    )
    return count
