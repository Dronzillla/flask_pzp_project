from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from openpyxl import load_workbook
from io import BytesIO
from flask_sqlalchemy import SQLAlchemy
from parse_project import ProjectParser


# db imports
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship


app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.db"
db: SQLAlchemy = SQLAlchemy(app)


# Forms file
class UploadForm(FlaskForm):
    file = FileField("Upload .xlsm file")
    submit = SubmitField("Upload")


# Models file
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy


class Project(db.Model):
    __tablename__ = "project"
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False, unique=True)
    code = Column(String(80), nullable=False, unique=True)

    general = relationship("General", uselist=False, back_populates="project")
    ratios = relationship("Ratios", uselist=False, back_populates="project")


class General(db.Model):
    __tablename__ = "general"
    id = Column(Integer, primary_key=True)
    start_date = Column(DateTime, nullable=False)
    reference_period = Column(Integer)
    analysis_method = Column(String(80))
    analysis_principle = Column(String(80))
    main_sector = Column(String(80))
    no_alternatives = Column(Integer)
    da_analysis = Column(Boolean, nullable=False)
    version = Column(String(80))

    project_id = Column(Integer, ForeignKey("project.id"), unique=True)
    project = relationship("Project", back_populates="general")


class Ratios(db.Model):
    __tablename__ = "ratios"
    id = Column(Integer, primary_key=True)
    enis = Column(Float)
    egdv = Column(Integer)
    evgn = Column(Float)
    sva = Column(Float)
    da = Column(Float)
    fgdv = Column(Integer)
    fvgn = Column(Float)
    fnis = Column(Float)

    project_id = Column(Integer, ForeignKey("project.id"), unique=True)
    project = relationship("Project", back_populates="ratios")


with app.app_context():
    db.create_all()


# db operations file
# Create new project
def db_create_project(name: str, code: str) -> bool:
    """Create new project in a database.
    Each project in database has unique name and code.
    If project with provided name and code does not exist, new project gets created.
    Otherwise, no new project is created.

    Args:
        name (str): Customer first name
        code (str): Customer last name
    Returns:
        bool: 'True' - Project with provided details does not exist, 'False' - Project with provided details exist.
    """
    # If project already exists, we should not create a new one
    if db_find_project_by_name(name) is not None:
        return False
    if db_find_project_by_code(code) is not None:
        return False

    # Create new project
    project = Project(name=name, code=code)
    db.session.add(project)
    db.session.commit()
    return True


def db_find_project_by_name(name: str) -> Project:
    """Checks if project exists in database based on an provided name.

    Args:
        name (str): Project name

    Returns:
        Project: 'Project' object if project exists in database, 'None' if project does not exist in database.
    """
    project = Project.query.filter_by(name=name).one_or_none()
    return project


def db_find_project_by_code(code: str) -> Project:
    """Checks if project exists in database based on an provided code.

    Args:
        name (str): Project code

    Returns:
        Project: 'Project' object if project exists in database, 'None' if project does not exist in database.
    """
    project = Project.query.filter_by(code=code).one_or_none()
    return project


# Routes file
@app.route("/", methods=["GET", "POST"])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        if file.filename.endswith(".xlsm"):
            # Read the file in memory
            in_memory_file = BytesIO(file.read())
            # Load workbook
            workbook = load_workbook(
                filename=in_memory_file, keep_vba=False, data_only=True
            )
            parser = ProjectParser(workbook=workbook)

            project = parser.fetch_project_info()
            db_create_project(name=project.name, code=project.code)

            date = 1
            return f"{date}"
        else:
            return "Only .xlsm files are allowed."
    return render_template("upload.html", form=form)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
