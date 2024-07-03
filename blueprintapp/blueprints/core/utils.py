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
    # print(df)
    return df


def convert_db_ratios_to_pd_df(ratios_data: list) -> pd.DataFrame:
    # Create a dictionary to hold the ratio and average values
    data = {row.ratio: row.average for row in ratios_data}
    # Create the DataFrame from the dictionary
    df = pd.DataFrame(data, index=["Value"])
    # Rename the first column
    # print(df)
    return df
