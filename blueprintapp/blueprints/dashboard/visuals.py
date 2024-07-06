from blueprintapp.blueprints.dashboard.db_operations import (
    db_read_cashflow_by_project_id,
    db_read_ratios_by_project_id,
    db_read_general_by_project_id,
    db_read_benefits_by_project_id,
)
from blueprintapp.utils.utilities import (
    pandas_convert_db_query_one_to_none_to_df,
    plotly_make_table_from_pandas_df,
)
import plotly.express as px
import pandas as pd


"""
Functions to make plotly graphs
"""


def graph_project_cashflows_scatter(project_id: int) -> str:
    """Create plotly scatter plot to graph project yearly cashflows.

    Returns:
        str: html string representation of a graph.
    """
    # Get data from db
    data = db_read_cashflow_by_project_id(project_id=project_id)
    if len(data) == 0:
        return ""
    # Convert db cashflow data to pandas DataFrame
    # df = convert_db_project_cashflows_to_pd_df(cashflow_data=data)
    # Convert db data to pandas DataFrame
    df = pd.DataFrame(data=data)
    # print(df)
    # Create graph for cashflows
    fig = px.scatter(df, x="year", y="amount", color="category")
    fig.update_layout(
        # title="Financial Cashflows by Category and Year",
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
    # print(df)
    # Create graph
    fig = px.scatter(df, x="year", y="amount", color="name")
    fig.update_layout(
        # title="Social Impact by Component and Year",
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


"""
Functions to make plotly tables
"""


def table_project_ratios(project_id: int) -> str:
    """Create plotly table to show ratios of a project.

    Returns:
        str: html string representation of a table.
    """
    # Get data from db
    data = db_read_ratios_by_project_id(project_id=project_id)
    if data is None:
        return ""
    # Convert db data to pandas DataFrame
    drop_columns = ["_sa_instance_state", "id", "project_id"]
    df = pandas_convert_db_query_one_to_none_to_df(data=data, drop_columns=drop_columns)
    # Create plotly figure
    fig = plotly_make_table_from_pandas_df(df=df)
    # Update layout of plotly figure
    fig.update_layout(
        height=70,
        margin=dict(t=0, b=0),
    )
    # # Create html table
    html_table = fig.to_html(full_html=False)
    return html_table


def table_project_general(project_id: int) -> str:
    """Create plotly table to show general information about project.

    Returns:
        str: html string representation of a table.
    """
    # Get data from db
    data = db_read_general_by_project_id(project_id=project_id)
    if data is None:
        return ""
    # Convert db data to pandas DataFrame
    drop_columns = ["_sa_instance_state", "id", "project_id"]
    df = pandas_convert_db_query_one_to_none_to_df(data=data, drop_columns=drop_columns)
    # Create plotly figure
    fig = plotly_make_table_from_pandas_df(df=df)
    # Update layout of plotly figure
    fig.update_layout(
        height=70,
        margin=dict(t=0, b=0),
    )
    # Create html table
    html_table = fig.to_html(full_html=False)
    return html_table


"""
ARCHIVE

def table_project_ratios(project_id: int) -> str:
    # Get db data for ratios
    data = db_read_ratios_by_project_id(project_id=project_id)
    if data is None:
        return ""
    # Convert db ratios data to pandas DataFrame
    df = convert_db_project_ratios_to_pd_df(ratios_data=data)
    # Set up header and cells for table
    header = dict(values=list(df.columns), align="left")
    cells = dict(
        values=[df[col] for col in df.columns],
        align="left",
    )
    fig = go.Figure(data=[go.Table(header=header, cells=cells)])
    fig.update_layout(
        # autosize=False,
        height=50,
        margin=dict(t=0, b=0),
    )
    # Create html table
    html_table = fig.to_html(full_html=False)
    return html_table
"""
