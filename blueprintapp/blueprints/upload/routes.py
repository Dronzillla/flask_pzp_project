from flask import request, render_template, redirect, url_for, Blueprint, flash
from flask_login import login_required, current_user
from blueprintapp.app import db  # Have to leave it for db migrations
from blueprintapp.blueprints.upload.models import (
    Project,
    General,
    Ratios,
    Cashflow,
    BenefitComponent,
    Benefit,
    HarmComponent,
    Harm,
)
from blueprintapp.blueprints.upload.parse_project import ProjectParser
from blueprintapp.blueprints.upload.forms import UploadForm
from blueprintapp.blueprints.upload.db_operations import (
    db_project_exists,
    db_create_project,
    db_assign_project_information,
    db_delete_all_projects,
    db_delete_sector_and_components,
)
from blueprintapp.blueprints.upload.utils import is_valid_excel_file


upload = Blueprint("upload", __name__, template_folder="templates")


# Only registered user can upload files
@upload.route("/", methods=["GET", "POST"])
@login_required
def index():
    form = UploadForm()
    # Get current user id
    user_id = current_user.id
    # if request.method == "POST":
    if form.validate_on_submit():
        file = form.file.data
        # Check if project is valid format
        workbook = is_valid_excel_file(file=file)
        if workbook is False:
            flash(
                "Upload failed. Only .xlsm or .xlsx files valid format excel spreadsheets are allowed.",
                "error",
            )
            return redirect(url_for("upload.index"))

        # Get data from excel spreadsheet
        parser = ProjectParser(workbook=workbook)
        project_data = parser.fetch_project_info()
        # Check if project is blank
        if project_data.name == "" or project_data.code == "":
            flash(
                "Upload failed. Project name and code are blank in uploaded file. ",
                "error",
            )
            return redirect(url_for("upload.index"))
        # Check if project exists in db
        if db_project_exists(project_tuple=project_data):
            flash("Upload failed. Project already exists. ", "info")
            return redirect(url_for("upload.index"))
        else:
            # Create new project
            project = db_create_project(project_tuple=project_data, user_id=user_id)
            # Get the remaining data from excel spreadsheet
            general_data = parser.fetch_general_info()
            ratios_data = parser.fetch_ratios()
            cashflows_data = parser.fetch_cashflows()
            benefits_data = parser.fetch_benefits()
            harms_data = parser.fetch_harms()
            economic_sectors_data = parser.fetch_economic_sectors()
            # Assign information to a project
            db_assign_project_information(
                project=project,
                general=general_data,
                ratios=ratios_data,
                cashflows=cashflows_data,
                benefits=benefits_data,
                harms=harms_data,
                economic_sector_names=economic_sectors_data,
            )
            flash("Upload successful. ", "info")
            return redirect(url_for("upload.index"))
    # if request.method == "GET":
    return render_template("upload/index.html", form=form)


# TODO Transfer routes to admin
@upload.route("/delete_all")
def delete_all():
    db_delete_all_projects()
    return redirect(url_for("core.index"))


@upload.route("/delete_sector")
def delete_all_sector():
    db_delete_sector_and_components()
    return redirect(url_for("core.index"))
