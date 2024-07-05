import pandas as pd
from blueprintapp.blueprints.upload.models import Ratios, General


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


def convert_db_project_ratios_to_pd_df(ratios_data: Ratios) -> pd.DataFrame:
    if ratios_data.fvgn == -9999.0:
        fvgn = "N/A"
    else:
        fvgn = ratios_data.fvgn

    data = {
        # "id": ratios_data.id,
        "ENIS": ratios_data.enis,
        "EGDV": ratios_data.egdv,
        "EVGN, %": ratios_data.evgn,
        "SVA": ratios_data.sva,
        "DA": ratios_data.da,
        "FGDV": ratios_data.fgdv,
        "FVGN, %": fvgn,
        "FNIS": ratios_data.fnis,
        # "project_id": ratios_data.project_id,
    }

    # ratio is column
    df = pd.DataFrame([data])
    # ratio is in rows
    # df = pd.DataFrame(list(data.items()), columns=["Ratio", "Value"])
    # print(df)
    return df


def convert_db_project_general_to_pd_df(general_data: General) -> pd.DataFrame:

    data = {
        # "id": general_data.id,
        "Start date": general_data.start_date,
        "Reference period": general_data.reference_period,
        "Analysis method": general_data.analysis_method,
        "Analysis principle": general_data.analysis_principle,
        "Main sector": general_data.main_sector,
        "Number of alternatives": general_data.no_alternatives,
        "Multicriteria analysis": general_data.da_analysis,
        "Spreadsheet version": general_data.version,
        # "project_id": general_data.project_id,
    }

    # ratio is column
    df = pd.DataFrame([data])
    # ratio is in rows
    # df = pd.DataFrame(list(data.items()), columns=["Indicator", "Value"])
    # print(df)
    return df


def convert_db_table_to_pd_df(data) -> pd.DataFrame:
    df = pd.DataFrame(data)
    return df
