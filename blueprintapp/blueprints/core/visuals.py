from blueprintapp.blueprints.core.db_operations import (
    db_aggregate_cashflow_data,
    db_aggregate_ratio_averages,
    db_aggregate_benefits_by_component_by_year,
    db_aggregate_general_analysis_methods_count,
    db_aggregate_general_analysis_principle_count,
    db_aggregate_general_main_sector_count,
)
from blueprintapp.blueprints.core.utils import (
    pandas_convert_db_ratios_to_df,
    pandas_filter_benefits_pd_df_top5,
)
from blueprintapp.utils.utilities import (
    plotly_make_table_from_pandas_df,
    plotly_update_layout_table_default,
    pandas_convert_db_query_all_to_df,
    pandas_sort_df_columns,
)
import plotly.graph_objects as go
import plotly.express as px


"""
Functions to make plotly graphs
"""


def graph_general_indicator_pie(indicator: str) -> str:
    """Create plotly pie chart to graph general indicator.

    Returns:
        str: html string representation of a graph or "-" is there is no data.
    """
    # Get database data from General models
    if indicator == "analysis_method":
        title = "Analysis Methods Used"
        data = db_aggregate_general_analysis_methods_count()
        legend_title = "Analysis method"
    elif indicator == "analysis_principle":
        title = "Analysis Principles Used"
        data = db_aggregate_general_analysis_principle_count()
        legend_title = "Analysis principle"
    elif indicator == "main_sector":
        title = "Main Economic Sectors"
        data = db_aggregate_general_main_sector_count()
        legend_title = "Main economic sector"
    if len(data) == 0:
        return "-"
    # Convert to pandas data frame
    df = pandas_convert_db_query_all_to_df(data=data)
    # Create general data count graph
    fig = px.pie(df, values="count", names=indicator)
    # fig = px.pie(df, values="count", names=indicator, title=title)
    # Make legend horizontal
    fig.update_layout(
        legend_title=legend_title,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    general_html_graph = fig.to_html(full_html=False)
    return general_html_graph


def graph_cashflows_scatter() -> str:
    """Create plotly scatter plot to graph aggregate yearly cashflows of all projects.

    Returns:
        str: html string representation of a graph or "-" if there is no data.
    """
    # Get database data for cashflows
    data = db_aggregate_cashflow_data()
    if len(data) == 0:
        return "-"
    # Convert db cashflow data to pandas data frame
    df = pandas_convert_db_query_all_to_df(data=data)
    # Create aggregate cashflows graph
    fig = px.scatter(df, x="year", y="total_amount", color="category")
    fig.update_layout(
        title="Aggregate Cashflows by Category and Year",
        xaxis_title="Year",
        yaxis_title="Amount",
        yaxis=dict(type="log"),
        legend_title="Category",
        barmode="group",
    )
    fig.update_traces(hovertemplate="Year: %{x}<br>Amount: %{y:.2s} EUR<br>")
    # Create HTML representation of the Plotly figure
    html_graph = fig.to_html(full_html=False)
    return html_graph


def graph_benefits_scatter_top5() -> str:
    """Create plotly scatter plot to graph aggregate yearly benefits of top5 benefit components.

    Returns:
        str: html string representation of a graph or "-" is there is no data.
    """
    # Get database data for cahsflows
    data = db_aggregate_benefits_by_component_by_year()
    if len(data) == 0:
        return "-"
    # Convert db benefits data to pandas Data Frame
    df = pandas_convert_db_query_all_to_df(data=data)
    # Get top 5 values
    df = pandas_filter_benefits_pd_df_top5(df=df)
    # Create aggregate benefits graph
    fig = px.scatter(df, x="year", y="total_amount", color="name")
    fig.update_layout(
        title="Top 5 Aggregate Benefits by Benefit Component and Year",
        xaxis_title="Year",
        yaxis_title="Amount",
        yaxis=dict(type="log"),
        # yaxis=dict(type="log", dtick=1, tickvals=y_ticks, ticktext=y_labels),
        legend_title="Component",
        barmode="group",
    )
    fig.update_traces(hovertemplate="Year: %{x}<br>Amount: %{y:.2s} EUR<br>")
    # Create HTML representation of the Plotly figure
    html_graph = fig.to_html(full_html=False)
    return html_graph


"""
Functions to make plotly tables
"""


def table_cashflows_totals() -> str:
    """Create plotly table to show aggregate yearly cashflows of all projects.

    Returns:
        str: html string representation of a table or "-" is there is no data.
    """
    # Get database data for cashflows
    data = db_aggregate_cashflow_data()
    if len(data) == 0:
        return "-"
    # Convert db cashflow data to pandas DataFrame
    df = pandas_convert_db_query_all_to_df(data=data)
    # Group by category and sum total_amount to show in millions
    category_sum = df.groupby("category")["total_amount"].sum() / 1000000
    category_sum = category_sum.round(0)
    # Set up header and cells for a table
    category_header = list(category_sum.index)
    values_header = list(category_sum.values)
    header = dict(values=category_header, align="left")
    cells = dict(values=values_header, align="left")
    # Create plotly table
    fig = go.Figure(data=[go.Table(header=header, cells=cells)])
    # Update table layout
    fig = plotly_update_layout_table_default(
        fig=fig, title="Aggregate Total Cashflows by Category in mil. Eur"
    )
    # Create HTML representation of the Plotly figure
    html_table = fig.to_html(full_html=False)
    return html_table


def table_ratios_averages() -> str:
    """Create plotly table to show average ratios values of all projects.

    Returns:
        str: html string representation of a table or "-" if there is no data.
    """
    # Get database data for ratios averages
    data = db_aggregate_ratio_averages()
    if len(data) == 0:
        return "-"
    # Convert db cashflow data to pandas DataFrame
    df = pandas_convert_db_ratios_to_df(ratios_data=data)
    # Sort df columns since in Dashboard ratios are sorted
    df = pandas_sort_df_columns(df=df)
    # Create plotly figure
    fig = plotly_make_table_from_pandas_df(
        df=df, title="Aggregate Average values of Ratios"
    )
    # Create html table
    html_table = fig.to_html(full_html=False)
    return html_table
