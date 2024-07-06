from flask import render_template, Blueprint
from blueprintapp.blueprints.core.visuals import (
    graph_cashflows_scatter,
    table_cashflows_totals,
    table_ratios_averages,
    graph_benefits_scatter_top5,
    graph_general_indicator_pie,
)
from blueprintapp.blueprints.core.db_operations import (
    db_aggregate_project_count,
)


core = Blueprint("core", __name__, template_folder="templates")


@core.route("/")
def index():
    project_count = db_aggregate_project_count()
    graph_cashflows_html = graph_cashflows_scatter()
    table_cashflows_html = table_cashflows_totals()
    table_ratios_html = table_ratios_averages()
    graph_benefits_html = graph_benefits_scatter_top5()
    graph_general_method_html = graph_general_indicator_pie(indicator="analysis_method")
    graph_general_principle_html = graph_general_indicator_pie(
        indicator="analysis_principle"
    )
    graph_general_sector_html = graph_general_indicator_pie(indicator="main_sector")

    return render_template(
        "core/index.html",
        project_count=project_count,
        graph_cashflows_html=graph_cashflows_html,
        table_cashflows_html=table_cashflows_html,
        table_ratios_html=table_ratios_html,
        graph_benefits_html=graph_benefits_html,
        graph_general_method_html=graph_general_method_html,
        graph_general_principle_html=graph_general_principle_html,
        graph_general_sector_html=graph_general_sector_html,
    )


@core.route("/about")
def about():
    return render_template("core/about.html")
