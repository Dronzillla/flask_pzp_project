from flask import request, render_template, redirect, url_for, Blueprint
from flask_login import login_required, current_user
from blueprintapp.app import db
from blueprintapp.blueprints.dashboard.db_operations import (
    db_read_all_user_projects,
    db_read_project_by_id_and_user_id,
    db_delete_project,
)
from blueprintapp.utils.utilities import flask_paginate_page_pagination


dashboard = Blueprint("dashboard", __name__, template_folder="templates")


@dashboard.route("/")
@login_required
def index():
    username = current_user.username
    projects = db_read_all_user_projects(user_id=current_user.id)
    # Set up project page pagination
    displayed_projects, pagination = flask_paginate_page_pagination(items=projects)
    return render_template(
        "dashboard/index.html",
        username=username,
        projects=displayed_projects,
        pagination=pagination,
    )


@dashboard.route("/project/delete/<int:id>")
@login_required
def delete_project(id):
    # Get user id
    user_id = current_user.id
    project = db_read_project_by_id_and_user_id(id=id, user_id=user_id)
    if project is None:
        return "Project not found", 404
    # Delete project
    db_delete_project(project)
    # Redirect to dashboard
    return redirect(url_for("dashboard.index"))
