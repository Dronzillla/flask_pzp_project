from blueprintapp.blueprints.core.db_operations import db_aggregate_cashflow_data
import pandas as pd


def convert_db_cashflow_to_pd_df(cashflow_data: list) -> pd.DataFrame:
    data = [
        {
            "year": row.year,
            "category": row.category,
            "total_amount": row.total_amount,
        }
        for row in cashflow_data
    ]
    df = pd.DataFrame(data)

    # Pivot the data to get years as rows and categories as columns
    df_pivot = df.pivot(index="year", columns="category", values="total_amount").fillna(
        0
    )
    return df_pivot
