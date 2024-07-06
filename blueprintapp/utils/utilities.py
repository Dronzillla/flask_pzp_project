from blueprintapp.app import db_column_map
import pandas as pd
import plotly.graph_objects as go


def pandas_convert_db_query_one_to_none_to_df(
    data, drop_columns: list[str]
) -> pd.DataFrame:
    """Convert database query where methods (.one_to_none, .first, .one) was used to pandas DataFrame. Also, maps column names to db_column_map.

    Args:
        data (_type_): query data.
        drop_columns (list[str]): list of column names in database table to delete.

    Returns:
        pd.DataFrame: pandas Dataframe without columns.
    """
    # Create pandas DataFrame
    df = pd.DataFrame([data.__dict__])
    # Drop columns
    df = df.drop(columns=drop_columns)
    df.rename(columns=db_column_map, inplace=True)
    # Sort columns
    df = df.reindex(sorted(df.columns), axis=1)
    return df


def plotly_make_table_from_pandas_df(df: pd.DataFrame) -> go.Figure:
    """Creates plotly table from pandas DataFrame, where each DataFrame column corresponds to column.

    Args:
        df (pd.DataFrame): pandas DataFrame.

    Returns:
        go.Figure: plotly table object.
    """
    header = dict(values=list(df.columns), align="left")
    cells = dict(
        values=[df[col] for col in df.columns],
        align="left",
    )
    fig = go.Figure(data=[go.Table(header=header, cells=cells)])
    return fig
