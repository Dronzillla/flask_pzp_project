from flask import request, render_template, redirect, url_for, Blueprint, flash
from flask_login import login_required, current_user
from blueprintapp.app import db
from blueprintapp.blueprints.dashboard.db_operations import (
    db_read_all_user_projects,
    db_read_project_by_id_and_user_id,
    db_delete_project,
    db_search_all_user_projects,
)
from blueprintapp.utils.utilities import flask_paginate_page_pagination
from blueprintapp.blueprints.projects.forms import SearchForm


dashboard = Blueprint("dashboard", __name__, template_folder="templates")


@dashboard.route("/", methods=["GET", "POST"])
@login_required
def index():
    form = SearchForm()
    search_query = None
    projects = []
    # POST method
    if form.validate_on_submit():
        search_query = form.query.data
        projects = db_search_all_user_projects(
            search_query=search_query, user_id=current_user.id
        )
        # If there are no projects flash a message.
        if search_query and not projects:
            flash("No projects found matching your query.")
    else:
        projects = db_read_all_user_projects(user_id=current_user.id)
    # Set up project page pagination
    displayed_projects, pagination = flask_paginate_page_pagination(items=projects)
    return render_template(
        "dashboard/index.html",
        projects=displayed_projects,
        pagination=pagination,
        form=form,
        search_query=search_query,
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
