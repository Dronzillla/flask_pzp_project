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
    # Plotly amd bootstrap css mappings
    PLOTLY_COLORS_GRAPHS = {
        "blue": "rgba(13, 110, 253, 0.75)",
        "red": "rgba(220, 53, 69, 0.75)",
        "green": "rgba(25, 135, 84, 0.75)",
        "yellow": "rgba(255, 193, 7, 0.75)",
        "indigo": "rgba(102, 16, 242, 0.75)",
        "purple": "rgba(111, 66, 193, 0.75)",
        "pink": "rgba(214, 51, 132, 0.75)",
        "orange": "rgba(253, 126, 20, 0.75)",
        "teal": "rgba(32, 201, 151, 0.75)",
        "cyan": "rgba(13, 202, 240, 0.75)",
    }
    PLOTLY_COLORS_TABLES = {
        "bg-secondary-subtle": "#e2e3e5",
        "bg-light": "#f8f9fa",
    }
    DB_COLUMN_MAP = {
        # General
        "start_date": "Start date",
        "reference_period": "Reference period",
        "analysis_method": "Analysis method",
        "analysis_principle": "Analysis principle",
        "main_sector": "Main sector",
        "no_alternatives": "Number of alternatives",
        "da_analysis": "Multicriteria analysis",
        "version": "Spreadsheet version",
        # Ratios
        "enis": "ENIS",
        "egdv": "EGDV",
        "evgn": "EVGN",
        "sva": "SVA",
        "da": "DA",
        "fgdv": "FGDV",
        "fvgn": "FVGN",
        "fnis": "FNIS",
        # Cashflows
        "capex": "Capital expenditure (CAPEX)",
        "reinvestment": "Reinvestments",
        "opex": "Operating expenditure (OPEX)",
        "revenue": "Revenue",
        "tax_revenue": "Revenue from taxes (without VAT)",
        "vat": "Value added tax (VAT) balance",
        "private_cf_cost": "Private sector CAPEX and OPEX",
        "private_cf_revenue": "Private sector revenue",
    }

    """
    ARCHIVE bootstrap color codes
    PLOTLY_COLORS_GRAPHS = {
        "blue": "#0d6efd",
        "red": "#dc3545",
        "green": "#198754",
        "yellow": "#ffc107",
        "indigo": "#6610f2",
        "purple": "#6f42c1",
        "pink": "#d63384",
        "orange": "#fd7e14",
        "teal": "#20c997",
        "cyan": "#0dcaf0",
    }
    """


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///./test.db"
