from blueprintapp.blueprints.dashboard.db_operations import (
    db_read_cashflow_by_project_id,
    db_read_ratios_by_project_id,
    db_read_general_by_project_id,
    db_read_benefits_by_project_id,
)
from blueprintapp.blueprints.dashboard.utils import (
    convert_db_project_cashflows_to_pd_df,
    convert_db_project_ratios_to_pd_df,
    convert_db_project_general_to_pd_df,
    convert_db_table_to_pd_df,
)
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def graph_project_cashflows_scatter(project_id: int) -> str:
    # Get database data for
    cashflow_data = db_read_cashflow_by_project_id(project_id=project_id)
    if len(cashflow_data) == 0:
        return ""
    # Convert db cashflow data to pandas DataFrame
    df = convert_db_project_cashflows_to_pd_df(cashflow_data=cashflow_data)
    # Create graph for cashflows
    fig = px.scatter(df, x="year", y="amount", color="category")
    fig.update_layout(
        title="Project Cashflows by Category and Year",
        xaxis_title="Year",
        yaxis_title="Amount",
        yaxis=dict(type="log"),
        legend_title="Category",
    )
    # Update hoover template
    fig.update_traces(hovertemplate="Year: %{x}<br>Amount: %{y:.2s} EUR<br>")
    # Create HTML graph
    cashflow_html_graph = fig.to_html(full_html=False)
    return cashflow_html_graph


def table_project_ratios(project_id: int) -> str:
    # Get db data for ratios
    ratios_data = db_read_ratios_by_project_id(project_id=project_id)
    if ratios_data is None:
        return ""
    # Convert db ratios data to pandas DataFrame
    df = convert_db_project_ratios_to_pd_df(ratios_data=ratios_data)
    # Set up header and cells for table
    header = dict(values=list(df.columns), align="left")
    cells = dict(
        values=[df[col] for col in df.columns],
        align="left",
    )
    fig = go.Figure(data=[go.Table(header=header, cells=cells)])
    # fig.update_layout(
    #     title="Project Ratios",
    #     height=200,
    #     margin=dict(b=10),
    # )

    fig.update_layout(
        # autosize=False,
        height=50,
        margin=dict(t=0, b=0),
    )

    # Create html table
    table_ratios_html = fig.to_html(full_html=False)
    return table_ratios_html


def table_project_general(project_id: int) -> str:
    # Get data from db
    data = db_read_general_by_project_id(project_id=project_id)
    print(data)
    if data is None:
        return ""
    # Convert db ratios data to pandas DataFrame
    df = convert_db_project_general_to_pd_df(general_data=data)
    # df = pd.DataFrame([data.__dict__])
    # Set up header and cells for table
    header = dict(values=list(df.columns), align="left")
    cells = dict(
        values=[df[col] for col in df.columns],
        align="left",
    )
    fig = go.Figure(data=[go.Table(header=header, cells=cells)])

    fig.update_layout(
        height=50,
        margin=dict(t=0, b=0),
    )
    # Create html table
    html_table = fig.to_html(full_html=False)
    # return ""
    return html_table


def graph_project_benefits_scatter(project_id: int):
    """Create plotly scatter plot to graph project yearly benefits.

    Returns:
        str: html string representation of a graph.
    """
    # Get data from db
    data = db_read_benefits_by_project_id(project_id=project_id)
    if len(data) == 0:
        return ""
    # Convert db data to pandas DataFrame
    df = pd.DataFrame(data=data)
    # Create graph
    fig = px.scatter(df, x="year", y="amount", color="name")
    fig.update_layout(
        title="Project Cashflows by Category and Year",
        xaxis_title="Year",
        yaxis_title="Amount",
        yaxis=dict(type="log"),
        legend_title="Component",
    )
    # Update hoover template
    fig.update_traces(hovertemplate="Year: %{x}<br>Amount: %{y:.2s} EUR<br>")
    # Create HTML graph
    html_graph = fig.to_html(full_html=False)
    return html_graph
