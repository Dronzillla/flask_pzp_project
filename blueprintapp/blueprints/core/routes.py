from flask import render_template, Blueprint
from blueprintapp.blueprints.core.visuals import (
    graph_cashflows_scatter,
    table_cashflows_totals,
)

core = Blueprint("core", __name__, template_folder="templates")


@core.route("/")
def index():
    plot_html = graph_cashflows_scatter()
    table_html = table_cashflows_totals()
    return render_template(
        "core/index.html", plot_html=plot_html, table_html=table_html
    )
