import pandas as pd


# =========================================================
# COLUMN SEMANTIC METADATA
# =========================================================

COLUMN_CONCEPTS = {

    "customer": {
        "description": "Identifies a customer or buyer.",
        "related_concepts": [
            "customer",
            "buyer",
            "client"
        ]
    },

    "city": {
        "description": "Geographic city or location associated with the record.",
        "related_concepts": [
            "city",
            "location",
            "place",
            "region"
        ]
    },

    "product": {
        "description": "Product or item associated with the transaction.",
        "related_concepts": [
            "product",
            "item",
            "goods",
            "merchandise"
        ]
    },

    "category": {
        "description": "Category or classification of the product or record.",
        "related_concepts": [
            "category",
            "type",
            "segment",
            "classification"
        ]
    },

    "quantity": {
        "description": "Number of units or items involved in the transaction.",
        "related_concepts": [
            "quantity",
            "units",
            "items",
            "volume",
            "unit count"
        ]
    },

    "total_amount": {
        "description": "Total monetary value associated with a transaction.",
        "related_concepts": [
            "amount",
            "sales",
            "revenue",
            "income",
            "transaction value"
        ]
    },

    "unit_price": {
        "description": "Price of one unit of the product or item.",
        "related_concepts": [
            "unit price",
            "price",
            "cost per unit",
            "item price"
        ]
    },

    "rating": {
        "description": "Rating or score associated with a product, service, or record.",
        "related_concepts": [
            "rating",
            "score",
            "review score",
            "evaluation"
        ]
    },

    "age": {
        "description": "Age associated with a person or customer.",
        "related_concepts": [
            "age",
            "customer age",
            "person age"
        ]
    },

    "purchase_month": {
        "description": "Month in which the purchase or event occurred.",
        "related_concepts": [
            "month",
            "purchase month",
            "monthly",
            "period"
        ]
    }
}


# =========================================================
# DETECT COLUMN ROLE
# =========================================================

def detect_column_role(
    column_name: str,
    column_data: pd.Series
) -> str:
    """
    Estimate the analytical role of a column.
    """

    name = column_name.lower().replace(
        "_",
        " "
    )


    # -----------------------------------------------------
    # TIME DIMENSIONS
    # -----------------------------------------------------

    time_keywords = {
        "date",
        "time",
        "month",
        "year",
        "quarter",
        "day"
    }

    if any(
        keyword in name
        for keyword in time_keywords
    ):

        return "time_dimension"


    # -----------------------------------------------------
    # IDENTIFIERS
    # -----------------------------------------------------

    identifier_keywords = {
        "id",
        "code",
        "identifier"
    }

    if (
        any(
            keyword in name
            for keyword in identifier_keywords
        )
        and not pd.api.types.is_numeric_dtype(
            column_data
        )
    ):

        return "identifier"


    # -----------------------------------------------------
    # NUMERIC COLUMNS
    # -----------------------------------------------------

    if pd.api.types.is_numeric_dtype(
        column_data
    ):

        numeric_name_keywords = {
            "amount",
            "price",
            "cost",
            "revenue",
            "sales",
            "quantity",
            "qty",
            "units",
            "salary",
            "income",
            "profit",
            "score",
            "rating"
        }

        if any(
            keyword in name
            for keyword in numeric_name_keywords
        ):

            return "measure"

        return "numeric_attribute"


    # -----------------------------------------------------
    # CATEGORICAL / TEXT COLUMNS
    # -----------------------------------------------------

    unique_count = column_data.nunique(
        dropna=True
    )

    if unique_count <= 20:

        return "categorical_dimension"

    return "text_attribute"


# =========================================================
# GET SEMANTIC METADATA
# =========================================================

def get_column_semantic_metadata(
    column_name: str
) -> dict:
    """
    Return semantic metadata for a column.

    Known business columns receive predefined
    descriptions and concepts.

    Unknown columns receive generic metadata.
    """

    normalized_name = (
        column_name
        .lower()
        .replace(
            " ",
            "_"
        )
    )


    if normalized_name in COLUMN_CONCEPTS:

        metadata = COLUMN_CONCEPTS[
            normalized_name
        ]

        return {
            "description": metadata[
                "description"
            ],

            "related_concepts": metadata[
                "related_concepts"
            ]
        }


    # -----------------------------------------------------
    # GENERIC FALLBACK
    # -----------------------------------------------------

    return {
        "description": (
            f"Column containing data related to "
            f"{column_name.replace('_', ' ')}."
        ),

        "related_concepts": [
            column_name.replace(
                "_",
                " "
            )
        ]
    }


# =========================================================
# PROFILE DATAFRAME
# =========================================================

def profile_dataframe(
    df: pd.DataFrame
) -> dict:
    """
    Generate schema, data-quality, analytical-role,
    and semantic metadata for an uploaded DataFrame.
    """

    profile = {
        "row_count": len(df),
        "column_count": len(df.columns),
        "columns": []
    }


    for column in df.columns:

        column_data = df[column]

        column_name = str(
            column
        )


        # -------------------------------------------------
        # COLUMN ROLE
        # -------------------------------------------------

        role = detect_column_role(
            column_name,
            column_data
        )


        # -------------------------------------------------
        # SEMANTIC METADATA
        # -------------------------------------------------

        semantic_metadata = (
            get_column_semantic_metadata(
                column_name
            )
        )


        # -------------------------------------------------
        # BASIC COLUMN INFORMATION
        # -------------------------------------------------

        column_info = {

            "name": column_name,

            "data_type": str(
                column_data.dtype
            ),

            "role": role,

            "description": (
                semantic_metadata[
                    "description"
                ]
            ),

            "related_concepts": (
                semantic_metadata[
                    "related_concepts"
                ]
            ),

            "missing_values": int(
                column_data.isnull().sum()
            ),

            "unique_values": int(
                column_data.nunique()
            ),

            "sample_values": (
                column_data
                .dropna()
                .head(5)
                .tolist()
            )
        }


        # -------------------------------------------------
        # NUMERIC RANGE
        # -------------------------------------------------

        if pd.api.types.is_numeric_dtype(
            column_data
        ):

            valid_values = (
                column_data
                .dropna()
            )

            if not valid_values.empty:

                column_info[
                    "minimum"
                ] = float(
                    valid_values.min()
                )

                column_info[
                    "maximum"
                ] = float(
                    valid_values.max()
                )

            else:

                column_info[
                    "minimum"
                ] = None

                column_info[
                    "maximum"
                ] = None

        else:

            column_info[
                "minimum"
            ] = None

            column_info[
                "maximum"
            ] = None


        # -------------------------------------------------
        # ADD COLUMN
        # -------------------------------------------------

        profile[
            "columns"
        ].append(
            column_info
        )


    return profile