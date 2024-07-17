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

# TODO Update website url
load_dotenv()
website_mail_username = os.getenv("MAIL_USERNAME_SECURED")
website_url = "www.flask-pzp-project.com"


"""
User password reset
"""


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


def email_send_reset_email(user: User) -> None:
    token = generate_reset_token(user=user)
    reset_url = url_for("auth.reset_password", token=token, _external=True)
    subject = "Password Reset Request"
    recipients = [user.email]
    body = f"""To reset your password at {website_url}, visit the following link: {reset_url}.
    \nIf you did not make this request, simply ignore this email and no changes will be made.
    """

    msg = Message(
        subject=subject, sender=website_mail_username, recipients=recipients, body=body
    )
    mail.send(msg)


"""
New user registration
An email is sent to registered user email. 
An email is sent to website and all admin emails.
"""


def email_user_new_user_registration(user: User) -> None:
    subject = "New user registration"
    recipients = [user.email]
    body = f"""You have successfully created an account at {website_url}. To log in and use the website's services, your account still needs to be verified by an administrator.
    \nKeep in mind that once your account is verified, you might not instantly receive an email notification.
    """

    msg = Message(
        subject=subject, sender=website_mail_username, recipients=recipients, body=body
    )
    mail.send(msg)


def email_admins_new_user_registration(user: User) -> None:
    subject = "New user awaits verification"
    # Recipients should be website email + all admin user emails
    admin_user_emails = db_read_admin_users_emails()
    # TODO update recipients to
    # recipients = [website_mail_username] + admin_user_emails
    recipients = [website_mail_username]
    body = f"New user with an email address {user.email} registered at {website_url} and awaits validation.\nLog in to the admin dashboard to validate user account."
    # Create new message and send emails.
    msg = Message(
        subject=subject, sender=website_mail_username, recipients=recipients, body=body
    )
    mail.send(msg)


"""
User verification
"""
# TODO make scenario when user verification emails are sent.


def email_user_account_verified(user: User) -> None:
    subject = "You account was verified"
    recipients = [user.email]
    body = f"Your account at {website_url} was verified. You can now log in and use the website services."

    msg = Message(
        subject=subject, sender=website_mail_username, recipients=recipients, body=body
    )
    mail.send(msg)
