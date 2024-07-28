import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from flask_paginate import Pagination, get_page_parameter
from flask import request, flash, abort, redirect, url_for
from flask_login import current_user
from functools import wraps
from flask import current_app
import textwrap


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
    Also, maps column names to DB_COLUMN_MAP and deletes specified columns.

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
    df.rename(columns=current_app.config["DB_COLUMN_MAP"], inplace=True)
    # Sort columns
    df = pandas_sort_df_columns(df=df)
    return df


def pandas_map_db_cashflows(df: pd.DataFrame) -> pd.DataFrame:
    """Maps list of columns in dataframe to user friendly names.

    Args:
        df (pd.DataFrame): pandas df with column 'category' where values are respective cashflow values in DB_COLUMN_MAP.

    Returns:
        pd.DataFrame: pandas DataFrame with converted values for cashflow categories in column 'category'.
    """
    df["category"] = df["category"].map(current_app.config["DB_COLUMN_MAP"])
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


def plotly_tables_colors_map() -> dict:
    """Gets default style colors for plotly table from config.py file.

    Returns:
        dict: a dictionary with bootstrap color name and color code for default table design.
    """
    # Access PLOTLY_COLORS_GRAPHS from the current application context
    colors = current_app.config["PLOTLY_COLORS_TABLES"]
    return colors


def plotly_make_table(header: dict, cells: dict, title: str = "") -> go.Figure:
    """Creates plotly table with provided header, cells and title values. Also, updates table header and cells color to match bootstrap color scheme.

    Args:
        header (dict): header items for table
        cells (dict): cells items for table
        title (str, optional): title for table if it exists. Defaults to "".

    Returns:
        go.Figure: plotly table object with colored to match bootstrap styling.
    """
    # Map default colors to a table
    colors = plotly_tables_colors_map()
    header["fill_color"] = colors.get("bg-secondary-subtle")
    cells["fill_color"] = colors.get("bg-light")
    # Create a table
    fig = go.Figure(data=[go.Table(header=header, cells=cells)])
    # Update table layout to default
    fig = plotly_update_layout_table_default(fig=fig, title=title)
    return fig


def plotly_make_table_from_pandas_df(df: pd.DataFrame, title: str = "") -> go.Figure:
    """Creates plotly table from pandas DataFrame, where each DataFrame column corresponds to column.

    Args:
        df (pd.DataFrame): pandas DataFrame.

    Returns:
        go.Figure: plotly table object with default height 80.
    """
    colors = plotly_tables_colors_map()
    header = dict(
        values=list(df.columns),
        align="left",
        fill_color=colors.get("bg-secondary-subtle"),
    )
    cells = dict(
        values=[df[col] for col in df.columns],
        align="left",
        fill_color=colors.get("bg-light"),
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
    # Update font family to fit bootstrap
    plotly_update_font_family_bootstrap(fig=fig)
    # Adjust layout to be fluid and responsive
    fig.update_layout(
        autosize=True,
        margin=dict(l=0, r=0, t=60 if title else 0, b=0),
        height=190 if title else 100,
        title=dict(text=plotly_wrap_text(text=title), y=0.92),
    )
    # Ensure the table is responsive
    fig.update_xaxes(automargin=True)
    fig.update_yaxes(automargin=True)
    return fig

    """
    ARCHIVE
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
    """


def plotly_update_layout_scatter_default(fig: go.Figure, title: str = "") -> None:
    """Make default scatter plot layout.

    Args:
        fig (go.Figure): plotly go.Figure object.
    """
    # Update font family to fit bootstrap
    plotly_update_font_family_bootstrap(fig=fig)
    # Update common layout features
    fig.update_layout(
        title=dict(text=plotly_wrap_text(text=title), y=0.96),
        yaxis=dict(type="log"),
        barmode="group",
        template="plotly_white",
        legend=dict(
            orientation="h",
            traceorder="reversed",
            x=0,
            y=-0.2,
        ),
    )
    # Update hoover template
    fig.update_traces(hovertemplate="Year: %{x}<br>Amount: %{y:.2s} EUR<br>")


def plotly_update_font_family_bootstrap(fig: go.Figure) -> None:
    """Updates plotly font-family and font-color to fit default bootstrap font styles.

    Args:
        fig (go.Figure): plotly figure.
    """
    font_family: str = (
        "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji'"
    )
    font_color: str = "#212529"
    font_properties = dict(family=font_family, color=font_color)
    fig.update_layout(font=font_properties, hoverlabel=dict(font=font_properties))


def plotly_graphs_colors_map() -> list:
    """Gets default style colors for plotly graph from config.py file.

    Returns:
        list: a list of color codes that matches default bootstrap style.
    """
    colors = current_app.config["PLOTLY_COLORS_GRAPHS"]
    result = list(colors.values())
    return result


def plotly_make_scatter(
    df: pd.DataFrame, x: str, y: str, color: str, title: str = ""
) -> go.Figure:
    """Create

    Args:
        df (pd.DataFrame): _description_
        x (str): _description_
        y (str): _description_
        color (str): _description_

    Returns:
        go.Figure: _description_
    """
    # Apply text wrapping to the legend values to make very long legend values fit mobile view
    df[color] = df[color].apply(lambda text: plotly_wrap_text(text))

    fig = px.scatter(
        data_frame=df,
        x=x,
        y=y,
        color=color,
        color_discrete_sequence=plotly_graphs_colors_map(),
    )
    plotly_update_layout_scatter_default(fig=fig, title=title)
    return fig


def flask_paginate_page_pagination(items) -> tuple:
    """Set up default page pagination using flask_paginate

    Args:
        items (_type_): any data items that should be paginated.

    Returns:
        tuple: displayed_items and 'Pagination' object
    """
    # Set up item pagination
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 5  # Number of items per page
    total = len(items)  # Total number of projects
    # Get projects for the current page
    start = (page - 1) * per_page
    end = start + per_page
    displayed_items = items[start:end]
    pagination = Pagination(
        page=page, per_page=per_page, total=total, css_framework="bootstrap5"
    )
    return (displayed_items, pagination)


def auth_is_valid_password(password: str) -> bool:
    """Checks for password strength. Password is at least 8 characters long, has at least 1 uppercase, 1 lowercase, 1 digit and 1 special character (!@#$%^&*()-_=+[{]};:'\",<.>/?).

    Args:
        password (str): Password as string

    Returns:
        bool: Returns 'True' if password strength is sufficient, 'False' if any condition is not met.
    """
    if len(password) < 8:
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char in "!@#$%^&*()-_=+[{]};:'\",<.>/?" for char in password):
        return False
    return True


def plotly_wrap_text(text: str) -> str:
    """Wraps text to fit into specific text width for mobile view

    Args:
        text (str): text to wrap

    Returns:
        str: wrapped text
    """
    # Wrap the title text for better display on mobile view
    wrapped_text = "<br>".join(textwrap.wrap(text, width=41))
    return wrapped_text


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)

    return decorated_function


def verified_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_verified:
            flash("You need to be verified to access this page.", "error")
            return redirect(url_for("core.index"))
        return f(*args, **kwargs)

    return decorated_function
