from dotenv import load_dotenv
import os

load_dotenv()
website_mail_username = os.getenv("MAIL_USERNAME_SECURED")
website_mail_password = os.getenv("MAIL_PASSWORD_SECURED")


class Config:
    SECRET_KEY = "your_secret_key"
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
