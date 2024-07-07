from flask import request, render_template, redirect, url_for, Blueprint, flash
from blueprintapp.app import db
from blueprintapp.blueprints.projects.visuals import (
    graph_project_cashflows_scatter,
    table_project_ratios,
    table_project_general,
    graph_project_benefits_scatter,
)
from blueprintapp.blueprints.projects.db_operations import (
    db_read_all_projects,
    db_read_project_by_id,
    db_search_all_projects,
)
from blueprintapp.utils.utilities import flask_paginate_page_pagination
from blueprintapp.blueprints.projects.forms import SearchForm


projects = Blueprint("projects", __name__, template_folder="templates")


@projects.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()
    search_query = None
    projects = []
    # POST method
    if form.validate_on_submit():
        search_query = form.query.data
        projects = db_search_all_projects(search_query)
        # If there are no projects flash a message.
        if search_query and not projects:
            flash("No projects found matching your query.")
    else:
        projects = db_read_all_projects()
    # Set up project page pagination
    displayed_projects, pagination = flask_paginate_page_pagination(items=projects)
    return render_template(
        "projects/index.html",
        projects=displayed_projects,
        pagination=pagination,
        form=form,
        search_query=search_query,
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
