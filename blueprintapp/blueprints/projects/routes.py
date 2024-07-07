from flask import request, render_template, redirect, url_for, Blueprint
from blueprintapp.app import db
from blueprintapp.blueprints.projects.visuals import (
    graph_project_cashflows_scatter,
    table_project_ratios,
    table_project_general,
    graph_project_benefits_scatter,
)
from blueprintapp.blueprints.projects.db_operations import (  # db read all projects
    db_read_all_projects,
    db_read_project_by_id,
)
from blueprintapp.utils.utilities import flask_paginate_page_pagination


projects = Blueprint("projects", __name__, template_folder="templates")


@projects.route("/")
def index():
    projects = db_read_all_projects()
    # Set up project page pagination
    displayed_projects, pagination = flask_paginate_page_pagination(items=projects)
    return render_template(
        "projects/index.html",
        projects=displayed_projects,
        pagination=pagination,
    )


@projects.route("/project/<int:id>")
def project(id):
    project = db_read_project_by_id(id=id)
    if project is None:
        return "Project not found", 404
    # Get project information from database.
    graph_cashflows_html = graph_project_cashflows_scatter(project_id=project.id)
    table_ratios_html = table_project_ratios(project_id=project.id)
    table_general_html = table_project_general(project_id=project.id)
    graph_benefits_html = graph_project_benefits_scatter(project_id=project.id)

    return render_template(
        "projects/project.html",
        project=project,
        graph_cashflows_html=graph_cashflows_html,
        table_ratios_html=table_ratios_html,
        table_general_html=table_general_html,
        graph_benefits_html=graph_benefits_html,
    )
