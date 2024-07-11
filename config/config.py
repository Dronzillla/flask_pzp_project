from dotenv import load_dotenv
import os

load_dotenv()
mail_username = os.getenv("MAIL_USERNAME_SECURED")
mail_password = os.getenv("MAIL_PASSWORD_SECURED")


class Config:
    SECRET_KEY = "your_secret_key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///./app.db"
    # Mail config
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = mail_username
    MAIL_PASSWORD = mail_password


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///./test.db"
