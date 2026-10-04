import pandas as pd
import plotly.graph_objects as go


# ============================================================
# PROFESSIONAL BI COLORS
# ============================================================

PRIMARY = "#2563EB"
SECONDARY = "#06B6D4"
SUCCESS = "#10B981"
WARNING = "#F59E0B"
PURPLE = "#8B5CF6"
PINK = "#EC4899"
ORANGE = "#F97316"

TEXT = "#111827"
MUTED = "#64748B"
GRID = "#E5E7EB"
BACKGROUND = "#FFFFFF"


# ============================================================
# BUSINESS-FRIENDLY COLUMN NAME
# ============================================================

def humanize_column_name(column_name):
    """
    Convert technical column names into readable
    business-friendly labels.

    Examples:

        total_amount
        -> Total Amount

        customer_age
        -> Customer Age

        purchase_month
        -> Purchase Month
    """

    name = str(column_name).strip()

    name = name.replace("_", " ")

    name = " ".join(
        name.split()
    )

    return name.title()


# ============================================================
# COMMON CHART STYLE
# ============================================================

def apply_style(
    fig,
    title,
    subtitle=None,
    x_title=None,
    y_title=None
):
    """
    Apply consistent professional styling
    to all Plotly charts.
    """

    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    if subtitle:

        title_text = (
            f"<b>{title}</b>"
            f"<br>"
            f"<span style='"
            f"font-size:13px;"
            f"color:{MUTED};"
            f"font-weight:400'>"
            f"{subtitle}"
            f"</span>"
        )

    else:

        title_text = (
            f"<b>{title}</b>"
        )


    # --------------------------------------------------------
    # MAIN LAYOUT
    # --------------------------------------------------------

    fig.update_layout(

        title={
            "text": title_text,
            "x": 0.02,
            "xanchor": "left",
            "y": 0.96,

            "font": {
                "family": "Arial",
                "size": 22,
                "color": TEXT
            }
        },

        font={
            "family": "Arial",
            "size": 13,
            "color": TEXT
        },

        paper_bgcolor=BACKGROUND,

        plot_bgcolor=BACKGROUND,

        margin={
            "l": 65,
            "r": 45,
            "t": 95,
            "b": 60
        },

        hoverlabel={
            "bgcolor": "#111827",

            "font": {
                "color": "#FFFFFF",
                "size": 13,
                "family": "Arial"
            }
        },

        hovermode="closest"
    )


    # --------------------------------------------------------
    # X AXIS
    # --------------------------------------------------------

    fig.update_xaxes(

        title_text=x_title,

        title_font={
            "color": TEXT,
            "size": 13
        },

        tickfont={
            "color": MUTED,
            "size": 12
        },

        showgrid=False,

        showline=True,

        linecolor=GRID,

        linewidth=1
    )


    # --------------------------------------------------------
    # Y AXIS
    # --------------------------------------------------------

    fig.update_yaxes(

        title_text=y_title,

        title_font={
            "color": TEXT,
            "size": 13
        },

        tickfont={
            "color": MUTED,
            "size": 12
        },

        showgrid=True,

        gridcolor=GRID,

        gridwidth=1,

        zeroline=False,

        showline=False
    )


    return fig


# ============================================================
# QUESTION INTENT
# ============================================================

def detect_intent(question):

    if not question:
        return "comparison"


    question = question.lower()


    # --------------------------------------------------------
    # TREND
    # --------------------------------------------------------

    if any(
        word in question
        for word in [
            "trend",
            "over time",
            "monthly",
            "month",
            "yearly",
            "year",
            "daily",
            "growth"
        ]
    ):

        return "trend"


    # --------------------------------------------------------
    # COMPOSITION
    # --------------------------------------------------------

    if any(
        word in question
        for word in [
            "percentage",
            "percent",
            "share",
            "proportion",
            "composition"
        ]
    ):

        return "composition"


    # --------------------------------------------------------
    # DISTRIBUTION
    # --------------------------------------------------------

    if any(
        word in question
        for word in [
            "distribution",
            "spread",
            "frequency"
        ]
    ):

        return "distribution"


    # --------------------------------------------------------
    # RELATIONSHIP
    # --------------------------------------------------------

    if any(
        word in question
        for word in [
            "relationship",
            "correlation",
            "related",
            "versus",
            "vs"
        ]
    ):

        return "relationship"


    # --------------------------------------------------------
    # RANKING
    # --------------------------------------------------------

    if any(
        word in question
        for word in [
            "top",
            "highest",
            "largest",
            "best"
        ]
    ):

        return "ranking"


    return "comparison"


# ============================================================
# DETECT MONTH COLUMN
# ============================================================

def detect_month_column(df):

    months = {
        "jan",
        "feb",
        "mar",
        "apr",
        "may",
        "jun",
        "jul",
        "aug",
        "sep",
        "oct",
        "nov",
        "dec"
    }


    for column in df.columns:

        values = (
            df[column]
            .dropna()
            .astype(str)
            .str.lower()
            .str[:3]
        )


        if len(values) == 0:
            continue


        matches = values.isin(
            months
        ).sum()


        if matches >= max(
            2,
            len(values) * 0.5
        ):

            return column


    return None


# ============================================================
# SORT MONTHS
# ============================================================

def sort_months(
    df,
    column
):

    month_order = [

        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec"

    ]


    result = df.copy()


    result[column] = (
        result[column]
        .astype(str)
        .str.title()
        .str[:3]
    )


    result[column] = pd.Categorical(
        result[column],
        categories=month_order,
        ordered=True
    )


    return result.sort_values(
        column
    )


# ============================================================
# PERCENTAGE RESULT DETECTION
# ============================================================

def is_percentage_result(
    df,
    value_column
):
    """
    Determine whether the numeric values represent
    percentages whose total is approximately 100.
    """

    if value_column not in df.columns:
        return False


    try:

        total = float(
            df[value_column].sum()
        )

    except (
        ValueError,
        TypeError
    ):

        return False


    return (
        99.0 <= total <= 101.0
    )


# ============================================================
# COMPOSITION TITLE
# ============================================================

def get_composition_title(
    user_question,
    category_column,
    value_column,
    percentage_result=False
):

    category_name = humanize_column_name(
        category_column
    )

    value_name = humanize_column_name(
        value_column
    )


    if percentage_result:

        return (
            f"Share of Total "
            f"{value_name} "
            f"by {category_name}"
        )


    if user_question:

        question = user_question.lower()


        if (
            "percentage" in question
            or "percent" in question
        ):

            return (
                f"Share of Total "
                f"{value_name} "
                f"by {category_name}"
            )


        if "share" in question:

            return (
                f"{value_name} "
                f"Share by "
                f"{category_name}"
            )


        if "proportion" in question:

            return (
                f"{value_name} "
                f"Proportion by "
                f"{category_name}"
            )


    return (
        f"{value_name} "
        f"by "
        f"{category_name}"
    )


# ============================================================
# BAR CHART
# ============================================================

def create_bar_chart(
    df,
    category_column,
    value_column,
    title,
    subtitle
):

    data = df.copy()


    # --------------------------------------------------------
    # SORT
    # --------------------------------------------------------

    data = data.sort_values(
        value_column,
        ascending=True
    )


    # --------------------------------------------------------
    # LIMIT VERY LARGE RESULTS
    # --------------------------------------------------------

    if len(data) > 12:

        data = data.tail(12)


    # --------------------------------------------------------
    # CREATE FIGURE
    # --------------------------------------------------------

    fig = go.Figure()


    fig.add_trace(

        go.Bar(

            x=data[value_column],

            y=data[category_column],

            orientation="h",

            marker={
                "color": PRIMARY,

                "line": {
                    "width": 0
                }
            },

            text=[
                f"{value:,.0f}"
                for value
                in data[value_column]
            ],

            textposition="outside",

            cliponaxis=False,

            hovertemplate=(

                "<b>%{y}</b>"
                "<br>"
                f"{humanize_column_name(value_column)}: "
                "%{x:,.2f}"
                "<extra></extra>"
            )
        )
    )


    fig.update_layout(
        showlegend=False
    )


    return apply_style(

        fig,

        title,

        subtitle,

        None,

        humanize_column_name(
            value_column
        )
    )


# ============================================================
# LINE CHART
# ============================================================

def create_line_chart(
    df,
    x_column,
    y_column,
    title,
    subtitle
):

    fig = go.Figure()


    fig.add_trace(

        go.Scatter(

            x=df[x_column],

            y=df[y_column],

            mode="lines+markers",

            line={
                "color": PRIMARY,
                "width": 3
            },

            marker={
                "size": 9,

                "color": PRIMARY,

                "line": {
                    "color": "#FFFFFF",
                    "width": 2
                }
            },

            fill="tozeroy",

            fillcolor=(
                "rgba(37,99,235,0.08)"
            ),

            hovertemplate=(

                "<b>%{x}</b>"
                "<br>"
                f"{humanize_column_name(y_column)}: "
                "%{y:,.2f}"
                "<extra></extra>"
            )
        )
    )


    return apply_style(

        fig,

        title,

        subtitle,

        humanize_column_name(
            x_column
        ),

        humanize_column_name(
            y_column
        )
    )


# ============================================================
# DONUT CHART
# ============================================================

def create_donut_chart(
    df,
    category_column,
    value_column,
    title,
    subtitle,
    percentage_result=False
):

    colors = [

        PRIMARY,
        ORANGE,
        SUCCESS,
        PURPLE,
        PINK,
        SECONDARY,
        WARNING

    ]


    fig = go.Figure()


    fig.add_trace(

        go.Pie(

            labels=df[category_column],

            values=df[value_column],

            hole=0.62,

            textinfo="percent",

            textposition="inside",

            sort=False,

            marker={

                "colors": colors[
                    :len(df)
                ],

                "line": {

                    "color": "#FFFFFF",

                    "width": 3
                }
            },

            hovertemplate=(

                "<b>%{label}</b>"
                "<br>"
                f"{humanize_column_name(value_column)}: "
                "%{value:,.2f}"
                "<br>"
                "Share: %{percent}"
                "<extra></extra>"
            )
        )
    )


    # --------------------------------------------------------
    # CENTER VALUE
    # --------------------------------------------------------

    total_value = float(
        df[value_column].sum()
    )


    if percentage_result:

        center_value = "100%"

        center_label = "Total Share"

    else:

        center_value = (
            f"{total_value:,.0f}"
        )

        center_label = "Total"


    fig.add_annotation(

        text=(

            f"<b>{center_value}</b>"
            "<br>"
            "<span style='"
            "font-size:12px;"
            "color:#64748B;"
            "font-weight:400'>"
            f"{center_label}"
            "</span>"
        ),

        x=0.5,

        y=0.5,

        showarrow=False,

        font={

            "family": "Arial",

            "size": 22,

            "color": TEXT
        },

        align="center"
    )


    # --------------------------------------------------------
    # LEGEND
    # --------------------------------------------------------

    fig.update_layout(

        showlegend=True,

        legend={

            "orientation": "v",

            "x": 0.82,

            "y": 0.5,

            "xanchor": "left",

            "yanchor": "middle",

            "font": {

                "family": "Arial",

                "size": 14,

                "color": TEXT
            },

            "bgcolor":
                "rgba(255,255,255,0)"
        },

        height=480,

        margin={

            "l": 20,

            "r": 180,

            "t": 95,

            "b": 30
        }
    )


    return apply_style(

        fig,

        title,

        subtitle
    )


# ============================================================
# HISTOGRAM
# ============================================================

def create_histogram(
    df,
    column,
    title,
    subtitle
):

    fig = go.Figure()


    fig.add_trace(

        go.Histogram(

            x=df[column],

            nbinsx=20,

            marker={

                "color": PRIMARY,

                "line": {

                    "color": "#FFFFFF",

                    "width": 1
                }
            },

            hovertemplate=(

                f"{humanize_column_name(column)}: "
                "%{x}"
                "<br>"
                "Count: "
                "%{y}"
                "<extra></extra>"
            )
        )
    )


    return apply_style(

        fig,

        title,

        subtitle,

        humanize_column_name(
            column
        ),

        "Count"
    )


# ============================================================
# BOX + POINTS CHART
# ============================================================

def create_box_points_chart(
    df,
    group_column,
    value_column,
    title,
    subtitle
):
    """
    Create a box plot with individual observations.

    Best for situations such as:

        Quantity = 1, 2, 3, 4
        Amount = different values

    This shows the distribution of Amount
    for every Quantity level.
    """

    data = df.copy()


    # --------------------------------------------------------
    # SORT GROUPS
    # --------------------------------------------------------

    try:

        data = data.sort_values(
            group_column
        )

    except Exception:

        pass


    fig = go.Figure()


    fig.add_trace(

        go.Box(

            x=data[group_column],

            y=data[value_column],

            name=humanize_column_name(
                value_column
            ),

            boxpoints="all",

            jitter=0.25,

            pointpos=0,

            marker={

                "color": PRIMARY,

                "size": 8,

                "opacity": 0.75,

                "line": {

                    "color": "#FFFFFF",

                    "width": 1
                }
            },

            line={

                "color": PRIMARY,

                "width": 2
            },

            fillcolor=(
                "rgba(37,99,235,0.12)"
            ),

            hovertemplate=(

                f"<b>"
                f"{humanize_column_name(group_column)}"
                f"</b>: "

                "%{x}"

                "<br>"

                f"<b>"
                f"{humanize_column_name(value_column)}"
                f"</b>: "

                "%{y:,.2f}"

                "<extra></extra>"
            )
        )
    )


    fig.update_layout(
        showlegend=False
    )


    return apply_style(

        fig,

        title,

        subtitle,

        humanize_column_name(
            group_column
        ),

        humanize_column_name(
            value_column
        )
    )


# ============================================================
# SCATTER CHART
# ============================================================

def create_scatter_chart(
    df,
    x_column,
    y_column,
    title,
    subtitle
):

    fig = go.Figure()


    fig.add_trace(

        go.Scatter(

            x=df[x_column],

            y=df[y_column],

            mode="markers",

            marker={

                "size": 11,

                "color": PRIMARY,

                "opacity": 0.75,

                "line": {

                    "color": "#FFFFFF",

                    "width": 1.5
                }
            },

            hovertemplate=(

                f"<b>"
                f"{humanize_column_name(x_column)}"
                f"</b>: "

                "%{x:,.2f}"

                "<br>"

                f"<b>"
                f"{humanize_column_name(y_column)}"
                f"</b>: "

                "%{y:,.2f}"

                "<extra></extra>"
            )
        )
    )


    return apply_style(

        fig,

        title,

        subtitle,

        humanize_column_name(
            x_column
        ),

        humanize_column_name(
            y_column
        )
    )


# ============================================================
# FIND COUNT/FREQUENCY COLUMN
# ============================================================

def find_count_column(
    numeric_columns
):

    count_names = {

        "count",
        "frequency",
        "freq",
        "number_of_customers",
        "customer_count",
        "order_count",
        "orders"

    }


    for column in numeric_columns:

        normalized = (
            str(column)
            .lower()
            .strip()
            .replace(" ", "_")
        )


        if normalized in count_names:

            return column


    return None


# ============================================================
# FIND DISCRETE NUMERIC COLUMN
# ============================================================

def find_discrete_numeric_column(
    df,
    numeric_columns,
    exclude_column=None
):
    """
    Find a numeric column with only a small number
    of distinct values.

    Example:

        Quantity = 1, 2, 3, 4

    This is ideal for a box + points chart.
    """

    candidates = []


    for column in numeric_columns:

        if column == exclude_column:

            continue


        unique_count = (
            df[column]
            .nunique(
                dropna=True
            )
        )


        if 2 <= unique_count <= 8:

            candidates.append(
                (
                    column,
                    unique_count
                )
            )


    if not candidates:

        return None


    # Prefer the column with
    # the smallest number of groups.

    candidates.sort(
        key=lambda item: item[1]
    )


    return candidates[0][0]


# ============================================================
# MAIN VISUALIZATION ENGINE
# ============================================================

def generate_chart(
    df: pd.DataFrame,
    user_question: str = None
):

    # --------------------------------------------------------
    # EMPTY RESULT
    # --------------------------------------------------------

    if df is None or df.empty:

        return None


    # --------------------------------------------------------
    # NUMERIC COLUMNS
    # --------------------------------------------------------

    numeric_columns = (

        df

        .select_dtypes(
            include="number"
        )

        .columns

        .tolist()

    )


    # --------------------------------------------------------
    # CATEGORICAL COLUMNS
    # --------------------------------------------------------

    categorical_columns = (

        df

        .select_dtypes(
            exclude="number"
        )

        .columns

        .tolist()

    )


    # --------------------------------------------------------
    # QUESTION INTENT
    # --------------------------------------------------------

    intent = detect_intent(
        user_question
    )


    # ========================================================
    # DISTRIBUTION HAS PRIORITY
    # ========================================================

    if intent == "distribution":

        # ----------------------------------------------------
        # CASE 1:
        # Age + Count
        # Quantity + Count
        # Rating + Count
        # ----------------------------------------------------

        if len(numeric_columns) >= 2:

            count_column = find_count_column(
                numeric_columns
            )


            if count_column is not None:

                other_columns = [

                    column

                    for column
                    in numeric_columns

                    if column != count_column

                ]


                if other_columns:

                    value_column = (
                        other_columns[0]
                    )


                    title = (

                        f"Distribution of "
                        f"{humanize_column_name(value_column)}"

                    )


                    return create_bar_chart(

                        df,

                        value_column,

                        count_column,

                        title,

                        (
                            f"Frequency of "
                            f"{humanize_column_name(value_column)}"
                        )

                    )


        # ----------------------------------------------------
        # CASE 2:
        # Raw numeric data
        # ----------------------------------------------------

        if len(numeric_columns) >= 1:

            value_column = (
                numeric_columns[0]
            )


            title = (

                f"Distribution of "
                f"{humanize_column_name(value_column)}"

            )


            return create_histogram(

                df,

                value_column,

                title,

                "Distribution of returned values"

            )


    # ========================================================
    # TREND
    # ========================================================

    if intent == "trend":

        month_column = detect_month_column(
            df
        )


        if (

            month_column is not None

            and

            len(numeric_columns) >= 1

        ):

            value_column = (
                numeric_columns[0]
            )


            sorted_df = sort_months(

                df,

                month_column

            )


            title = (

                f"{humanize_column_name(value_column)} "
                f"Trend"

            )


            return create_line_chart(

                sorted_df,

                month_column,

                value_column,

                title,

                "Monthly performance over time"

            )


    # ========================================================
    # COMPOSITION
    # ========================================================

    if (

        intent == "composition"

        and

        len(numeric_columns) >= 1

        and

        len(categorical_columns) >= 1

        and

        len(df) <= 8

    ):

        value_column = (
            numeric_columns[0]
        )

        category_column = (
            categorical_columns[0]
        )


        percentage_result = (
            is_percentage_result(
                df,
                value_column
            )
        )


        title = get_composition_title(

            user_question,

            category_column,

            value_column,

            percentage_result

        )


        if percentage_result:

            subtitle = (

                "Percentage contribution "
                f"by "
                f"{humanize_column_name(category_column)}"

            )

        else:

            subtitle = (

                "Contribution by "
                f"{humanize_column_name(category_column)}"

            )


        return create_donut_chart(

            df,

            category_column,

            value_column,

            title,

            subtitle,

            percentage_result

        )


    # ========================================================
    # RELATIONSHIP
    # ========================================================

    if (

        intent == "relationship"

        and

        len(numeric_columns) >= 2

    ):

        # ----------------------------------------------------
        # Check whether one variable is discrete.
        #
        # Example:
        #
        # Quantity = 1,2,3,4
        # Amount = many values
        #
        # Use box + points.
        # ----------------------------------------------------

        discrete_column = (
            find_discrete_numeric_column(
                df,
                numeric_columns
            )
        )


        if discrete_column is not None:

            other_columns = [

                column

                for column
                in numeric_columns

                if column != discrete_column

            ]


            if other_columns:

                value_column = (
                    other_columns[0]
                )


                title = (

                    f"{humanize_column_name(value_column)} "
                    f"by "
                    f"{humanize_column_name(discrete_column)}"

                )


                subtitle = (

                    f"Distribution across "
                    f"{humanize_column_name(discrete_column)} "
                    f"levels"

                )


                return create_box_points_chart(

                    df,

                    discrete_column,

                    value_column,

                    title,

                    subtitle

                )


        # ----------------------------------------------------
        # Continuous numeric relationship
        # ----------------------------------------------------

        x_column = (
            numeric_columns[0]
        )

        y_column = (
            numeric_columns[1]
        )


        title = (

            f"{humanize_column_name(y_column)} "
            f"vs "
            f"{humanize_column_name(x_column)}"

        )


        return create_scatter_chart(

            df,

            x_column,

            y_column,

            title,

            "Relationship between numeric measures"

        )


    # ========================================================
    # TWO NUMERIC COLUMNS WITHOUT RELATIONSHIP WORDS
    # ========================================================

    if len(numeric_columns) >= 2:

        discrete_column = (
            find_discrete_numeric_column(
                df,
                numeric_columns
            )
        )


        if discrete_column is not None:

            other_columns = [

                column

                for column
                in numeric_columns

                if column != discrete_column

            ]


            if other_columns:

                value_column = (
                    other_columns[0]
                )


                title = (

                    f"{humanize_column_name(value_column)} "
                    f"by "
                    f"{humanize_column_name(discrete_column)}"

                )


                return create_box_points_chart(

                    df,

                    discrete_column,

                    value_column,

                    title,

                    (
                        f"Distribution across "
                        f"{humanize_column_name(discrete_column)} "
                        f"levels"
                    )

                )


        x_column = (
            numeric_columns[0]
        )

        y_column = (
            numeric_columns[1]
        )


        return create_scatter_chart(

            df,

            x_column,

            y_column,

            (
                f"{humanize_column_name(y_column)} "
                f"vs "
                f"{humanize_column_name(x_column)}"
            ),

            "Relationship between numeric measures"

        )


    # ========================================================
    # ONE NUMERIC + ONE CATEGORICAL
    # ========================================================

    if (

        len(numeric_columns) >= 1

        and

        len(categorical_columns) >= 1

    ):

        value_column = (
            numeric_columns[0]
        )

        category_column = (
            categorical_columns[0]
        )


        # ----------------------------------------------------
        # RANKING
        # ----------------------------------------------------

        if intent == "ranking":

            top_data = (

                df

                .sort_values(

                    value_column,

                    ascending=False

                )

                .head(10)

            )


            title = (

                f"Top {len(top_data)} "
                f"by "
                f"{humanize_column_name(value_column)}"

            )


            return create_bar_chart(

                top_data,

                category_column,

                value_column,

                title,

                (
                    f"Ranked by "
                    f"{humanize_column_name(value_column)}"
                )

            )


        # ----------------------------------------------------
        # DEFAULT COMPARISON
        # ----------------------------------------------------

        title = (

            f"{humanize_column_name(value_column)} "
            f"by "
            f"{humanize_column_name(category_column)}"

        )


        return create_bar_chart(

            df,

            category_column,

            value_column,

            title,

            (
                f"Comparison across "
                f"{humanize_column_name(category_column)}"
            )

        )


    # ========================================================
    # ONE NUMERIC COLUMN
    # ========================================================

    if len(numeric_columns) == 1:

        value_column = (
            numeric_columns[0]
        )


        return create_histogram(

            df,

            value_column,

            (
                f"Distribution of "
                f"{humanize_column_name(value_column)}"
            ),

            "Distribution of returned values"

        )


    # ========================================================
    # ONLY CATEGORICAL DATA
    # ========================================================

    if len(categorical_columns) >= 1:

        category_column = (
            categorical_columns[0]
        )


        counts = (

            df[category_column]

            .value_counts()

            .reset_index()

        )


        counts.columns = [

            category_column,

            "count"

        ]


        counts = counts.head(10)


        return create_bar_chart(

            counts,

            category_column,

            "count",

            (
                f"Distribution of "
                f"{humanize_column_name(category_column)}"
            ),

            "Most frequent categories"

        )


    # ========================================================
    # NO SUITABLE CHART
    # ========================================================

    return None