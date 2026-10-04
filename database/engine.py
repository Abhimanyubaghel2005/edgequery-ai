import sqlite3

import pandas as pd
from sql.validator import validate_sql

def create_database():

    connection = sqlite3.connect(":memory:")

    return connection


def load_dataframe_to_database(
    df: pd.DataFrame,
    connection: sqlite3.Connection,
    table_name: str = "dataset"
):

    df.to_sql(
        table_name,
        connection,
        if_exists="replace",
        index=False
    )


def execute_query(
    query: str,
    connection: sqlite3.Connection
):

    is_safe, message = validate_sql(query)

    if not is_safe:

        raise ValueError(
            f"SQL query rejected: {message}"
        )

    result = pd.read_sql_query(
        query,
        connection
    )

    return result