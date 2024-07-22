import pandas as pd
from flask import current_app
from blueprintapp.blueprints.upload.parse_project import ProjectParser


def pandas_convert_db_ratios_to_df(ratios_data: list) -> pd.DataFrame:
    """Converts db query result that calculates the average values for each ratio to pandas DataFrame.

    Args:
        ratios_data (list): list of named tuples to store ratio values.

    Returns:
        pd.DataFrame: pandas DataFrame that has ratios mapped with "DB_COLUMN_MAP".
    """
    # Create a dictionary to hold the ratio and average values
    data = {
        row.ratio: ProjectParser.round_ratio(ratio=row.average, ratio_name=row.ratio)
        for row in ratios_data
    }
    # Create the DataFrame from the dictionary
    df = pd.DataFrame(data, index=["Value"])
    # Rename columns
    df.rename(columns=current_app.config["DB_COLUMN_MAP"], inplace=True)
    return df


def pandas_filter_benefits_pd_df_top5(df: pd.DataFrame) -> pd.DataFrame:
    """Filter pandas DataFrame to get benefit data of only 5 unique benefits that has maximum sum values over all years.

    Args:
        df (pd.DataFrame): not filrered pandas DataFrame.

    Returns:
        pd.DataFrame: filtered pandas DataFrame.
    """
    summed_df = df.groupby("name", as_index=False)["total_amount"].sum()
    # Identify the top 5 names based on summed total_amount
    top5_names = summed_df.nlargest(5, "total_amount")["name"]
    # Filter the original DataFrame to keep only rows corresponding to the top 5 names
    filtered_df = df[df["name"].isin(top5_names)]
    return filtered_df
