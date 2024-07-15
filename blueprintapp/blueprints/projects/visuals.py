from blueprintapp.blueprints.projects.db_operations import (
    db_read_cashflow_by_project_id,
    db_read_ratios_by_project_id,
    db_read_general_by_project_id,
    db_read_benefits_by_project_id,
    db_read_project_by_id,
)
from blueprintapp.utils.utilities import (
    pandas_convert_db_query_one_to_none_to_df,
    plotly_make_table_from_pandas_df,
    plotly_make_scatter,
)
import pandas as pd


"""
Functions to make plotly graphs for specific project
"""


def graph_project_cashflows_scatter(project_id: int) -> str:
    """Create plotly scatter plot to graph project yearly cashflows.

    Returns:
        str: html string representation of a graph.
    """
    # Get data from db
    data = db_read_cashflow_by_project_id(project_id=project_id)
    if len(data) == 0:
        return "-"
    # Convert db data to pandas DataFrame
    df = pd.DataFrame(data=data)
    # Create graph for cashflows
    fig = plotly_make_scatter(df=df, x="year", y="amount", color="category")
    # Update graph with specific properties
    fig.update_layout(
        title=f"Progress Plan No. {db_read_project_by_id(id=project_id).code} Financial Cashflows by Category and Year",
        xaxis_title="Year",
        yaxis_title="Amount",
        legend_title="Category",
    )
    # Create HTML graph
    html_graph = fig.to_html(full_html=False)
    return html_graph


def graph_project_benefits_scatter(project_id: int) -> str:
    """Create plotly scatter plot to graph project yearly benefits.

    Returns:
        str: html string representation of a graph.
    """
    # Get data from db
    data = db_read_benefits_by_project_id(project_id=project_id)
    if len(data) == 0:
        return "-"
    # Convert db data to pandas DataFrame
    df = pd.DataFrame(data=data)
    # Create graph
    fig = plotly_make_scatter(df=df, x="year", y="amount", color="name")
    fig.update_layout(
        title=f"Progress Plan No. {db_read_project_by_id(id=project_id).code} Social Impact by Component and Year",
        xaxis_title="Year",
        yaxis_title="Amount",
        legend_title="Component",
    )
    # Create HTML graph
    html_graph = fig.to_html(full_html=False)
    return html_graph


"""
Functions to make plotly tables for specific project
"""


def table_project_ratios(project_id: int) -> str:
    """Create plotly table to show ratios of a project.

    Returns:
        str: html string representation of a table or "-" if there is no data.
    """
    # Get data from db
    data = db_read_ratios_by_project_id(project_id=project_id)
    if data is None:
        return "-"
    # Convert db data to pandas DataFrame
    drop_columns = ["_sa_instance_state", "id", "project_id"]
    df = pandas_convert_db_query_one_to_none_to_df(data=data, drop_columns=drop_columns)
    # Create plotly figure
    fig = plotly_make_table_from_pandas_df(
        df=df,
        title=f"Progress Plan No. {db_read_project_by_id(id=project_id).code} Financial and Economic Ratios Values",
    )
    # Add an annotation for explaining ratios
    fig.update_layout(
        annotations=[
            dict(
                text="Note! If the ratio value is '-9999', the ratio calculation was not successful. If the ratio value is 'null', the ratio should not have been calculated.",
                y=0,
                showarrow=False,
            )
        ]
    )
    # Create html table
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
    fig = plotly_make_table_from_pandas_df(
        df=df,
        title=f"Progress Plan No. {db_read_project_by_id(id=project_id).code} General Information",
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
