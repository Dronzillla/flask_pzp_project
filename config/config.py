from dotenv import load_dotenv
import os

load_dotenv()
website_mail_username = os.getenv("MAIL_USERNAME_SECURED")
website_mail_password = os.getenv("MAIL_PASSWORD_SECURED")
secret_key = os.getenv("SECRET_KEY")
security_password_salt = os.getenv("SECURITY_PASSWORD_SALT")


class Config:
    # TODO Update secret key
    SECRET_KEY = secret_key
    SECURITY_PASSWORD_SALT = security_password_salt
    SQLALCHEMY_DATABASE_URI = "sqlite:///./app.db"
    # Mail config
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = website_mail_username
    MAIL_PASSWORD = website_mail_password


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///./test.db"
