from flask import request, render_template, redirect, url_for, Blueprint

# Have to leave it for db migrations
from blueprintapp.app import db
from blueprintapp.blueprints.upload.models import Project, General, Ratios

from blueprintapp.blueprints.upload.db_operations import db_create_project

# Routes import
from openpyxl import load_workbook
from io import BytesIO

#
from blueprintapp.blueprints.upload.parse_project import ProjectParser

#
from blueprintapp.blueprints.upload.forms import UploadForm

upload = Blueprint("upload", __name__, template_folder="templates")


# Routes file
@upload.route("/", methods=["GET", "POST"])
def index():
    form = UploadForm()

    if request.method == "POST":
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

                # Get data from excel spreadsheet

                general = parser.fetch_general_info()
                cashflows = parser.fetch_cashflows()
                ratios = parser.fetch_ratios()

                benefits = parser.fetch_benefits()
                harms = parser.fetch_harms()

                economic_sectors = parser.fetch_economic_sectors()

                project = parser.fetch_project_info()

                # Test db operations
                project = db_create_project(name=project.name, code=project.code)
                # print(project.id)

                # db_assign_general(
                #     start_date=general.start_date,
                #     reference_period=general.reference_period,
                #     analysis_method=general.analysis_method,
                #     analysis_principle=general.analysis_principle,
                #     main_sector=general.main_sector,
                #     no_alternatives=general.no_alternatives,
                #     da_analysis=general.da_analysis,
                #     version=general.version,
                #     project_id=project.id,
                # )

                date = 1
                return f"{date}"
            else:
                return "Only .xlsm files are allowed."
        # return render_template("upload/index.html", form=form)
    return render_template("upload/index.html", form=form)


# @upload.route("/")
# def index():
#     upload = Todo.query.all()
#     # Create a directory in templates that use same name as blueprint
#     return render_template("upload/index.html", upload=upload)


# @upload.route("/create", methods=["GET", "POST"])
# def create():
#     if request.method == "GET":
#         return render_template("upload/create.html")
#     elif request.method == "POST":
#         title = request.form.get("title")
#         description = request.form.get("description")
#         # If checkbox is checked
#         done = True if "done" in request.form.keys() else False
#         # If decsription is empty string set it to None
#         description = description if description != "" else None
#         todo = Todo(title=title, description=description, done=done)
#         db.session.add(todo)
#         db.session.commit()
#         return redirect(url_for("upload.index"))
