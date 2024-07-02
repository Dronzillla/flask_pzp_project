from blueprintapp.blueprints.dashboard.db_operations import (
    db_read_cashflow_by_project_id,
    db_read_ratios_by_project_id,
)
from blueprintapp.blueprints.dashboard.utils import (
    convert_db_project_cashflows_to_pd_df,
    convert_db_project_ratios_to_pd_df,
)
import plotly.express as px
import plotly.graph_objects as go


def graph_project_cashflows_scatter(project_id: int) -> str:
    # Get database data for cashflows
    cashflow_data = db_read_cashflow_by_project_id(project_id=project_id)
    if len(cashflow_data) == 0:
        return ""
    # Convert db cashflow data to pandas DataFrame
    df = convert_db_project_cashflows_to_pd_df(cashflow_data=cashflow_data)
    # Create graph for cashflows
    fig = px.scatter(df, x="year", y="amount", color="category")
    fig.update_layout(
        title="Cashflow by Category and Year",
        xaxis_title="Year",
        yaxis_title="Amount",
        yaxis=dict(type="log"),
        legend_title="Category",
    )
    # Update hoover template
    fig.update_traces(hovertemplate="Year: %{x}<br>Amount: %{y:.2s} EUR<br>")

    # Create HTML representation of the Plotly figure
    cashflow_html_graph = fig.to_html(full_html=False)
    return cashflow_html_graph


def table_project_ratios(project_id: int) -> str:
    # Get db data for ratios
    ratios_data = db_read_ratios_by_project_id(project_id=project_id)
    if ratios_data is None:
        return ""
    # Convert db ratios data to pandas DataFrame
    df = convert_db_project_ratios_to_pd_df(ratios_data=ratios_data)

    fig = go.Figure(
        data=[
            go.Table(
                header=dict(values=list(df.columns), align="left"),
                cells=dict(
                    values=[
                        df[col] for col in df.columns
                    ],  # Provide each column's data
                    align="left",
                ),
            )
        ]
    )
    # TODO remake this to include table
    # fig.show()
