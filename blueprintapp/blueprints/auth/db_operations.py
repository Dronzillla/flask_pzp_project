from blueprintapp.app import db
from blueprintapp.blueprints.auth.models import User
from typing import Optional
from flask_login import current_user


def db_read_user_by_email(email: str) -> Optional[User]:
    user = User.query.filter_by(email=email).first()
    return user


def db_create_new_user(username: str, email: str, password: str) -> User:
    user = User(username=username, email=email, is_admin=False, is_verified=False)
    user.set_password(password=password)
    db.session.add(user)
    db.session.commit()
    return user


def db_update_current_user_password(password: str) -> None:
    current_user.set_password(password=password)
    db.session.commit()


def db_update_user_password(user: User, password: str) -> None:
    user.set_password(password=password)
    db.session.commit()


def db_delete_user(user: User) -> None:
    db.session.delete(user)
    db.session.commit()


def db_read_user_by_id(id: int) -> Optional[User]:
    result = User.query.filter_by(id=id).one_or_none()
    return result


def db_admin_user_created(username: str, email: str, password: str) -> bool:
    # Check if user with provided email already exists
    existing_user = db_read_user_by_email(email=email)
    if existing_user:
        return False
    # If not create new admin user
    user = User(username=username, email=email, is_admin=True, is_verified=True)
    user.set_password(password=password)
    db.session.add(user)
    db.session.commit()
    return True


def db_read_admin_users_emails() -> list:
    result = User.query.with_entities(User.email).filter_by(is_admin=True).all()
    return [email for (email,) in result]
