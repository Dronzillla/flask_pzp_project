import pandas as pd
from flask import current_app
from blueprintapp.blueprints.upload.parse_project import ProjectParser


def pandas_convert_db_ratios_to_df(ratios_data: list) -> pd.DataFrame:
    # Map ndigits to round ratios
    # Create a dictionary to hold the ratio and average values
    data = {
        row.ratio: ProjectParser.round_ratio(ratio=row.average, ratio_name=row.ratio)
        for row in ratios_data
    }
    # print(data)
    # Create the DataFrame from the dictionary
    df = pd.DataFrame(data, index=["Value"])
    # print(df)
    # Rename columns
    df.rename(columns=current_app.config["DB_COLUMN_MAP"], inplace=True)
    return df


def pandas_filter_benefits_pd_df_top5(df: pd.DataFrame) -> pd.DataFrame:
    summed_df = df.groupby("name", as_index=False)["total_amount"].sum()
    # Identify the top 5 names based on summed total_amount
    top5_names = summed_df.nlargest(5, "total_amount")["name"]
    # Filter the original DataFrame to keep only rows corresponding to the top 5 names
    filtered_df = df[df["name"].isin(top5_names)]
    return filtered_df


"""
ARCHIVE
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
    # print(df)
    return df


def convert_db_general_to_df(general_data: list) -> pd.DataFrame:
    df = pd.DataFrame(general_data)
    # print(df)
    return df

    
def convert_db_benefits_to_pd_df(benefits_data: list) -> pd.DataFrame:
    data = [
        {
            "year": row.year,
            "name": row.name,
            "total_amount": row.total_amount,
        }
        for row in benefits_data
    ]
    df = pd.DataFrame(data)
    # print(df)
    return df


def convert_db_list_to_pd_df(data: list) -> pd.DataFrame:
    df = pd.DataFrame(data)
    # print(df)
    return df
"""
