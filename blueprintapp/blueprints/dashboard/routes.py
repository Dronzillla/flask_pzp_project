from flask import request, render_template, redirect, url_for, Blueprint
from flask_login import login_required, current_user
from blueprintapp.app import db
from blueprintapp.blueprints.dashboard.db_operations import (
    db_read_all_user_projects,
    db_read_project_by_id,
    db_delete_project,
)
from blueprintapp.blueprints.dashboard.visuals import (
    graph_project_cashflows_scatter,
    table_project_ratios,
    table_project_general,
    graph_project_benefits_scatter,
)


dashboard = Blueprint("dashboard", __name__, template_folder="templates")


@dashboard.route("/")
@login_required
def index():
    username = current_user.username
    projects = db_read_all_user_projects(user_id=current_user.id)
    return render_template("dashboard/index.html", username=username, projects=projects)


@dashboard.route("/project/<int:id>")
@login_required
def project(id):

    # TODO Make View and Delete as buttons
    # Get user id
    user_id = current_user.id
    project = db_read_project_by_id(id=id, user_id=user_id)
    if project is None:
        return "Project not found", 404
    # TODO Get project information from database.
    graph_cashflows_html = graph_project_cashflows_scatter(project_id=project.id)
    table_ratios_html = table_project_ratios(project_id=project.id)
    table_general_html = table_project_general(project_id=project.id)
    graph_benefits_html = graph_project_benefits_scatter(project_id=project.id)

    return render_template(
        "dashboard/project.html",
        project=project,
        graph_cashflows_html=graph_cashflows_html,
        table_ratios_html=table_ratios_html,
        table_general_html=table_general_html,
        graph_benefits_html=graph_benefits_html,
    )


@dashboard.route("/project/delete/<int:id>")
@login_required
def delete_project(id):
    # Get user id
    user_id = current_user.id
    project = db_read_project_by_id(id=id, user_id=user_id)
    if project is None:
        return "Project not found", 404
    # Delete project
    db_delete_project(project)
    # Redirect to dashboard
    return redirect(url_for("dashboard.index"))
