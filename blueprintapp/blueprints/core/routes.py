from flask import render_template, Blueprint
from blueprintapp.blueprints.core.visuals import (
    graph_cashflows_scatter,
    table_cashflows_totals,
    table_ratios_averages,
    graph_benefits_scatter_top5,
)

core = Blueprint("core", __name__, template_folder="templates")


@core.route("/")
def index():
    plot_html = graph_cashflows_scatter()
    table_html = table_cashflows_totals()
    ratios_html = table_ratios_averages()
    graph_benefits_html = graph_benefits_scatter_top5()
    return render_template(
        "core/index.html",
        plot_html=plot_html,
        table_html=table_html,
        ratios_html=ratios_html,
        graph_benefits_html=graph_benefits_html,
    )
