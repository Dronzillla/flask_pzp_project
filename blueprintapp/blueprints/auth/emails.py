from blueprintapp.app import mail
from flask_mail import Message
from blueprintapp.blueprints.auth.db_operations import db_read_admin_users_emails
from dotenv import load_dotenv
import os

load_dotenv()
website_mail_username = os.getenv("MAIL_USERNAME_SECURED")


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
