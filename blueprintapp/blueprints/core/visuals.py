from blueprintapp.blueprints.core.db_operations import db_aggregate_cashflow_data
from blueprintapp.blueprints.core.utils import convert_db_cashflow_to_pd_df
import plotly.graph_objects as go
import plotly.express as px


def graph_cashflows_scatter() -> str:
    # Get database data for cahsflows
    cashflow_data = db_aggregate_cashflow_data()
    if len(cashflow_data) == 0:
        return ""
    # Convert db cashflow data to pandas data frame
    df_pivot = convert_db_cashflow_to_pd_df(cashflow_data=cashflow_data)
    # Create aggregate cashflows graph
    fig = px.scatter(df_pivot, x="year", y="total_amount", color="category")
    fig.update_layout(
        title="Aggregate Cashflow by Category and Year",
        xaxis_title="Year",
        yaxis_title="Amount",
        yaxis=dict(type="log"),
        # yaxis=dict(type="log", dtick=1, tickvals=y_ticks, ticktext=y_labels),
        legend_title="Category",
        barmode="group",
    )
    fig.update_traces(hovertemplate="Year: %{x}<br>Amount: %{y:.2s} EUR<br>")
    # Create HTML representation of the Plotly figure
    cashflow_html_graph = fig.to_html(full_html=False)
    return cashflow_html_graph


def table_cashflows_totals() -> str:
    # Get database data for cashflows
    cashflow_data = db_aggregate_cashflow_data()
    if len(cashflow_data) == 0:
        return ""
    # Convert db cashflow data to pandas DataFrame
    df = convert_db_cashflow_to_pd_df(cashflow_data=cashflow_data)
    # Group by category and sum total_amount to show in millions
    category_sum = df.groupby("category")["total_amount"].sum() / 1000000
    category_sum = category_sum.round(0)
    # Set up header and cells for table
    header = dict(values=list(category_sum.index), align="left")
    cells = dict(values=list(category_sum.values), align="left")
    # Create the Plotly table
    fig = go.Figure(data=[go.Table(header=header, cells=cells)])
    fig.update_layout(
        # autosize=False,
        height=50,
        margin=dict(t=0, b=0),
    )
    cashflow_html_table = fig.to_html(full_html=False)
    return cashflow_html_table
