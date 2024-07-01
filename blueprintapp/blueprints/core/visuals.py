from blueprintapp.blueprints.core.db_operations import db_aggregate_cashflow_data
from blueprintapp.blueprints.core.utils import convert_db_cashflow_to_pd_df
import plotly.graph_objects as go
import pandas as pd


def graph_cashflows_scatter() -> str:
    # Get database data for cahsflows
    cashflow_data = db_aggregate_cashflow_data()
    if len(cashflow_data) == 0:
        return ""
    # Convert db cashflow data to pandas data frame
    df_pivot = convert_db_cashflow_to_pd_df(cashflow_data=cashflow_data)

    # Set up y axis for graph
    y_ticks = [0, 100, 100**2, 100**3, 100**4, 100**5, 100**6]
    y_labels = [
        "0 EUR",
        "100 EUR",
        "10,000 EUR",
        "1 mill. EUR",
        "100 mill. EUR",
        "10 bill. EUR",
    ]
    fig = go.Figure()

    for category in df_pivot.columns:
        fig.add_trace(
            go.Scatter(
                x=df_pivot.index,
                y=df_pivot[category],
                mode="markers",
                name=category,
                # fill="tozeroy",
            )
        )

    fig.update_layout(
        title="Aggregate Cashflow by Category and Year",
        xaxis_title="Year",
        yaxis_title="Amount",
        yaxis=dict(type="log", dtick=1, tickvals=y_ticks, ticktext=y_labels),
        legend_title="Category",
        barmode="group",
    )

    # Create HTML representation of the Plotly figure
    cashflow_html_graph = fig.to_html(full_html=False)
    return cashflow_html_graph


def table_cashflows_totals() -> str:
    # Get database data for cashflows
    cashflow_data = db_aggregate_cashflow_data()
    if len(cashflow_data) == 0:
        return ""

    # Convert db cashflow data to pandas DataFrame
    df_pivot = convert_db_cashflow_to_pd_df(cashflow_data=cashflow_data)

    # Calculate the totals for all columns
    sum_row = df_pivot.sum().rename("Total")
    # Divide by million to get value in millions
    df_pivot = pd.concat([df_pivot, pd.DataFrame([sum_row / 1000000])])
    # Filter to include only the "Total" row
    df_pivot = round(df_pivot.loc[["Total"]], 0)

    # Create Plotly table
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=["Year"] + list(df_pivot.columns),
                    align="left",
                ),
                cells=dict(
                    values=[df_pivot.index]
                    + [df_pivot[col] for col in df_pivot.columns],
                    align="left",
                ),
            )
        ]
    )
    # Update layout for the table
    fig.update_layout(
        title="Cashflow Data, Total (mill. Eur)",
    )
    # Create HTML representation of the Plotly table
    cashflow_html_table = fig.to_html(full_html=False)
    return cashflow_html_table


# def table_cashflows() -> str:
#     # Get database data for cahsflows
#     cashflow_data = db_aggregate_cashflow_data()
#     # Convert db cashflow data to pandas data frame
#     df_pivot = convert_db_cashflow_to_pd_df(cashflow_data=cashflow_data)
#     # Sum each column and add it as a new row
#     sum_row = df_pivot.sum().rename("Total")
#     df_pivot = pd.concat([df_pivot, pd.DataFrame([sum_row])])
#     # Filter to include only the "Total" row
#     df_total_only = df_pivot.loc[["Total"]]

#     table_html = df_pivot.to_html(
#         classes="table table-striped", float_format="{:,.0f}".format
#     )
#     return table_html
