from flask import url_for, current_app
from flask_mail import Message
from blueprintapp.blueprints.auth.db_operations import (
    db_read_admin_users_emails,
    db_read_user_by_email,
)
from blueprintapp.blueprints.auth.models import User
from blueprintapp.app import mail
from dotenv import load_dotenv
import os
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from typing import Optional

# TODO Remake with current_app.config
load_dotenv()
website_mail_username = os.getenv("MAIL_USERNAME_SECURED")


def generate_reset_token(user: User, expires_sec=1800) -> str:
    s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return s.dumps(user.email, salt=current_app.config["SECURITY_PASSWORD_SALT"])


def verify_reset_token(token, expires_sec=1800) -> Optional[User]:
    s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        email = s.loads(
            token,
            salt=current_app.config["SECURITY_PASSWORD_SALT"],
            max_age=expires_sec,
        )
    except (SignatureExpired, BadSignature):
        return None
    return db_read_user_by_email(email=email)


def mail_admins_new_user_registration(email: str) -> None:
    subject = "New user awaits validation"
    # Recipients should be website email + all admin user emails
    admin_user_emails = db_read_admin_users_emails()
    # TODO update recipients to
    # recipients = [website_mail_username] + admin_user_emails
    recipients = [website_mail_username]
    body = f"New user with an email address {email} registered and awaits validation. Log in to admin dashboard to validate user account. \n \nThis email was sent by flask-pzp-project app. "
    # Create new message and send to admin user emails.
    msg = Message(subject=subject, sender=website_mail_username, recipients=recipients)
    msg.body = body
    mail.send(msg)


def mail_send_reset_email(user: User):
    token = generate_reset_token(user=user)
    reset_url = url_for("auth.reset_password", token=token, _external=True)
    subject = "Password Reset Request"
    msg = Message(
        subject=subject, sender=website_mail_username, recipients=[user.email]
    )
    msg.body = f"""To reset your password, visit the following link:
{reset_url}
If you did not make this request, simply ignore this email and no changes will be made.
"""
    mail.send(msg)
