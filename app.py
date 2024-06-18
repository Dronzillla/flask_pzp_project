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

            project_info = parser.fetch_project_info()

            date = 1
            return f"{date}"
        else:
            return "Only .xlsm files are allowed."
    return render_template("upload.html", form=form)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
