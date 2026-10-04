def add_column_to_context(
    context: list,
    column: dict
):
    """
    Add complete information about one column
    to the schema context.
    """

    context.append(
        f"\nColumn: {column['name']}"
    )

    context.append(
        f"Data Type: {column['data_type']}"
    )

    context.append(
        f"Role: {column['role']}"
    )

    context.append(
        f"Meaning: {column['description']}"
    )

    context.append(
        f"Related Concepts: {column['related_concepts']}"
    )

    context.append(
        f"Missing Values: {column['missing_values']}"
    )

    context.append(
        f"Unique Values: {column['unique_values']}"
    )

    context.append(
        f"Sample Values: {column['sample_values']}"
    )

    if column["minimum"] is not None:

        context.append(
            f"Minimum: {column['minimum']}"
        )

    if column["maximum"] is not None:

        context.append(
            f"Maximum: {column['maximum']}"
        )


def build_schema_context(
    profile: dict,
    table_name: str = "dataset"
) -> str:
    """
    Convert the complete schema profile into
    structured semantic context for an LLM.
    """

    context = []

    context.append(
        f"Table: {table_name}"
    )

    context.append(
        f"Rows: {profile['row_count']}"
    )

    context.append(
        f"Columns: {profile['column_count']}"
    )

    context.append(
        "\nColumn Details:"
    )

    for column in profile["columns"]:

        add_column_to_context(
            context,
            column
        )

    return "\n".join(context)


def build_relevant_schema_context(
    profile: dict,
    relevant_columns: list[str],
    table_name: str = "dataset"
) -> str:
    """
    Build schema context using only the columns
    relevant to the user's question.
    """

    context = []

    context.append(
        f"Table: {table_name}"
    )

    context.append(
        "\nRelevant Column Details:"
    )

    for column in profile["columns"]:

        if column["name"] not in relevant_columns:
            continue

        add_column_to_context(
            context,
            column
        )

    return "\n".join(context)