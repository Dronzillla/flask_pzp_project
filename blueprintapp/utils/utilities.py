from blueprintapp.app import db_column_map
import pandas as pd
import plotly.graph_objects as go


def pandas_sort_df_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Sorts pandas DataFrame by columns.

    Args:
        df (pd.DataFrame): pandas DataFrame.

    Returns:
        pd.DataFrame: pandas DataFrame with sorted columns.
    """
    df = df.reindex(sorted(df.columns), axis=1)
    return df


def pandas_convert_db_query_one_to_none_to_df(
    data, drop_columns: list[str] = []
) -> pd.DataFrame:
    """Convert database query where methods (.one_to_none, .first, .one) was used to pandas DataFrame.
    Also, maps column names to db_column_map and deletes specified columns.

    Args:
        data (_type_): query data. Can be any model.
        drop_columns (list[str]): list of column names in database table to delete.

    Returns:
        pd.DataFrame: pandas Dataframe without specified columns.
    """
    # Create pandas DataFrame
    df = pd.DataFrame([data.__dict__])
    # Drop columns
    df = df.drop(columns=drop_columns)
    df.rename(columns=db_column_map, inplace=True)
    # Sort columns
    df = pandas_sort_df_columns(df=df)
    return df


def pandas_convert_db_query_all_to_df(data) -> pd.DataFrame:
    """Convert database query where method (.all) was used to pandas DataFrame.

    Args:
        data (_type_): query data. Can be any model.

    Returns:
        pd.DataFrame: pandas DataFrame.
    """
    df = pd.DataFrame(data)
    return df


def plotly_make_table_from_pandas_df(df: pd.DataFrame, title: str = "") -> go.Figure:
    """Creates plotly table from pandas DataFrame, where each DataFrame column corresponds to column.

    Args:
        df (pd.DataFrame): pandas DataFrame.

    Returns:
        go.Figure: plotly table object with default height 80.
    """
    header = dict(values=list(df.columns), align="left")
    cells = dict(
        values=[df[col] for col in df.columns],
        align="left",
    )
    fig = go.Figure(data=[go.Table(header=header, cells=cells)])
    # Update table layout to default
    fig = plotly_update_layout_table_default(fig=fig, title=title)
    return fig


def plotly_update_layout_table_default(fig: go.Figure, title: str = "") -> go.Figure:
    """Make default table layout for height and margin and set table title.

    Args:
        fig (go.Figure): plotly go.Figure object.
        title (str, optional): title of a table. Defaults to "".

    Returns:
        go.Figure: updated plotly go.Figure object.
    """
    if title == "":
        fig.update_layout(
            height=100,
            margin=dict(t=0, b=0),
        )
        return fig
    else:
        fig.update_layout(
            title=title,
            height=180,
            margin=dict(t=60, b=0),
        )
        return fig
