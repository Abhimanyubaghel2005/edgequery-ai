import sqlglot

from sqlglot import exp


# =========================================================
# ALLOWED STATEMENTS
# =========================================================

ALLOWED_STATEMENTS = (
    exp.Select,
    exp.Union,
)


# =========================================================
# BLOCKED STATEMENTS
# =========================================================

BLOCKED_STATEMENTS = (
    exp.Insert,
    exp.Update,
    exp.Delete,
    exp.Drop,
    exp.Create,
    exp.Alter,
)


# =========================================================
# BASIC SQL VALIDATION
# =========================================================

def validate_sql(
    query: str
) -> tuple[bool, str]:
    """
    Validate SQL before execution.

    Checks:

    1. Query is not empty.
    2. SQL syntax is valid.
    3. Only one statement is allowed.
    4. Dangerous statements are blocked.
    5. Only SELECT/UNION queries are allowed.
    """

    query = query.strip()

    if not query:

        return (
            False,
            "SQL query cannot be empty."
        )

    try:

        statements = sqlglot.parse(
            query,
            dialect="sqlite"
        )

    except Exception as error:

        return (
            False,
            f"Invalid SQL syntax: {error}"
        )

    if len(statements) != 1:

        return (
            False,
            "Only one SQL statement is allowed."
        )

    statement = statements[0]

    if isinstance(
        statement,
        BLOCKED_STATEMENTS
    ):

        return (
            False,
            f"{type(statement).__name__} "
            "statements are not allowed."
        )

    if not isinstance(
        statement,
        ALLOWED_STATEMENTS
    ):

        return (
            False,
            "Only SELECT queries are allowed."
        )

    return (
        True,
        "SQL is safe."
    )


# =========================================================
# EXTRACT COLUMN REFERENCES
# =========================================================

def extract_column_names(
    query: str
) -> set[str]:
    """
    Extract column names referenced by a SQL query.

    SQL aliases are excluded.

    Example:

        SELECT
            city,
            SUM(total_amount) AS total_revenue
        FROM dataset
        GROUP BY city
        ORDER BY total_revenue DESC

    Returns:

        {'city', 'total_amount'}
    """

    try:

        expression = sqlglot.parse_one(
            query,
            dialect="sqlite"
        )

    except Exception:

        return set()


    # -----------------------------------------------------
    # FIND SQL ALIASES
    # -----------------------------------------------------

    aliases = set()

    for alias in expression.find_all(
        exp.Alias
    ):

        alias_name = alias.alias

        if alias_name:

            aliases.add(
                alias_name.lower()
            )


    # -----------------------------------------------------
    # FIND COLUMN REFERENCES
    # -----------------------------------------------------

    columns = set()

    for column in expression.find_all(
        exp.Column
    ):

        column_name = column.name

        if not column_name:
            continue

        # -----------------------------------------------
        # IGNORE SQL ALIASES
        # -----------------------------------------------

        if column_name.lower() in aliases:
            continue

        columns.add(
            column_name
        )


    return columns


# =========================================================
# VALIDATE COLUMN REFERENCES
# =========================================================

def validate_column_references(
    query: str,
    allowed_columns: list[str]
) -> tuple[bool, str]:
    """
    Verify that SQL references only columns
    available in the uploaded dataset.

    SQL aliases are allowed.

    Example:

        SUM(total_amount) AS total_revenue

    total_amount must exist in the dataset.

    total_revenue does NOT need to exist because
    it is a SQL-generated alias.
    """

    # -----------------------------------------------------
    # BASIC SQL VALIDATION
    # -----------------------------------------------------

    is_safe, message = validate_sql(
        query
    )

    if not is_safe:

        return (
            False,
            message
        )


    # -----------------------------------------------------
    # NORMALIZE DATASET COLUMNS
    # -----------------------------------------------------

    allowed_columns_normalized = {
        str(column).lower()
        for column in allowed_columns
    }


    # -----------------------------------------------------
    # EXTRACT ACTUAL COLUMN REFERENCES
    # -----------------------------------------------------

    referenced_columns = (
        extract_column_names(
            query
        )
    )


    # -----------------------------------------------------
    # FIND UNKNOWN COLUMNS
    # -----------------------------------------------------

    unknown_columns = {

        column

        for column in referenced_columns

        if column.lower()
        not in allowed_columns_normalized
    }


    # -----------------------------------------------------
    # REJECT UNKNOWN COLUMNS
    # -----------------------------------------------------

    if unknown_columns:

        return (
            False,
            "SQL references unknown column(s): "
            + ", ".join(
                sorted(
                    unknown_columns
                )
            )
        )


    # -----------------------------------------------------
    # VALID
    # -----------------------------------------------------

    return (
        True,
        "SQL column references are valid."
    )