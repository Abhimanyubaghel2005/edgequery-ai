import re


BUSINESS_SYNONYMS = {
    "city": {
        "city",
        "cities",
        "location",
        "locations",
        "place",
    },

    "total_amount": {
        "total_amount",
        "total amount",
        "amount",
        "sales",
        "revenue",
        "income",
    },

    "quantity": {
        "quantity",
        "qty",
        "units",
        "unit",
        "number of items",
    },

    "customer": {
        "customer",
        "customers",
        "buyer",
        "buyers",
    },

    "product": {
        "product",
        "products",
        "item",
        "items",
    },

    "category": {
        "category",
        "categories",
        "type",
        "segment",
    },

    "age": {
        "age",
        "ages",
    },

    "rating": {
        "rating",
        "ratings",
        "review score",
        "score",
    },

    "purchase_month": {
        "purchase_month",
        "purchase month",
        "month",
        "monthly",
    }
}


def normalize_text(text: str) -> set[str]:
    """
    Convert text into normalized words.
    """

    text = text.lower()
    text = text.replace("_", " ")

    return set(
        re.findall(
            r"\b\w+\b",
            text
        )
    )


def get_column_score(
    user_question: str,
    column: str
) -> int:
    """
    Calculate how strongly a column is related
    to the user's question.
    """

    question_words = normalize_text(
        user_question
    )

    column_words = normalize_text(
        column
    )

    score = 0

    # ------------------------------------------------
    # 1. DIRECT COLUMN MATCH
    # ------------------------------------------------

    if column_words.issubset(question_words):

        score += 5

    elif question_words.intersection(
        column_words
    ):

        score += 2

    # ------------------------------------------------
    # 2. BUSINESS SYNONYM MATCH
    # ------------------------------------------------

    if column in BUSINESS_SYNONYMS:

        for synonym in BUSINESS_SYNONYMS[column]:

            synonym_words = normalize_text(
                synonym
            )

            if synonym_words.issubset(
                question_words
            ):

                score += 5

            elif question_words.intersection(
                synonym_words
            ):

                score += 2

    # ------------------------------------------------
    # 3. GENERIC CUSTOMER MATCH PENALTY
    # ------------------------------------------------

    if column in {
        "customer_id",
        "customer_name"
    }:

        if "customer" in question_words:

            # Customer is only a concept here.
            # Do not treat it as a request for
            # customer_id or customer_name.
            score -= 3

    return score


def retrieve_relevant_columns(
    user_question: str,
    columns: list[str]
) -> list[str]:
    """
    Find the most relevant columns for a user question.
    """

    scored_columns = []

    for column in columns:

        score = get_column_score(
            user_question,
            column
        )

        if score > 0:

            scored_columns.append(
                (column, score)
            )

    # ------------------------------------------------
    # SORT BY SCORE
    # ------------------------------------------------

    scored_columns.sort(
        key=lambda item: item[1],
        reverse=True
    )

    if not scored_columns:
        return []

    # ------------------------------------------------
    # KEEP STRONG AND MEANINGFUL MATCHES
    # ------------------------------------------------

    highest_score = scored_columns[0][1]

    relevant_columns = []

    for column, score in scored_columns:

        if score >= 4:

            relevant_columns.append(
                column
            )

        elif score == highest_score:

            relevant_columns.append(
                column
            )

    return relevant_columns