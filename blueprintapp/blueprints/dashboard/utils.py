import pandas as pd


def convert_db_project_cashflows_to_pd_df(cashflow_data: list) -> pd.DataFrame:
    data = [
        {
            "year": row.year,
            "category": row.category,
            "amount": row.amount,
        }
        for row in cashflow_data
    ]
    df = pd.DataFrame(data)
    # print(df)
    return df


def convert_db_project_ratios_to_pd_df(ratios_data) -> pd.DataFrame:
    data = {
        "id": ratios_data.id,
        "enis": ratios_data.enis,
        "egdv": ratios_data.egdv,
        "evgn": ratios_data.evgn,
        "sva": ratios_data.sva,
        "da": ratios_data.da,
        "fgdv": ratios_data.fgdv,
        "fvgn": ratios_data.fvgn,
        "fnis": ratios_data.fnis,
        "project_id": ratios_data.project_id,
    }

    df = pd.DataFrame([data])
    print(df)
    return df
