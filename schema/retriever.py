import re


# =========================================================
# BUSINESS SYNONYMS
# =========================================================

BUSINESS_SYNONYMS = {

    "city": {
        "city",
        "cities",
        "location",
        "locations",
        "place",
        "region"
    },

    "total_amount": {
        "total_amount",
        "total amount",
        "amount",
        "sales",
        "revenue",
        "income",
        "transaction value"
    },

    "quantity": {
        "quantity",
        "qty",
        "units",
        "unit",
        "number of items",
        "unit count",
        "volume"
    },

    "customer": {
        "customer",
        "customers",
        "buyer",
        "buyers",
        "client"
    },

    "product": {
        "product",
        "products",
        "item",
        "items",
        "goods",
        "merchandise"
    },

    "category": {
        "category",
        "categories",
        "type",
        "segment",
        "classification"
    },

    "age": {
        "age",
        "ages",
        "customer age",
        "person age"
    },

    "rating": {
        "rating",
        "ratings",
        "review score",
        "score",
        "evaluation"
    },

    "purchase_month": {
        "purchase_month",
        "purchase month",
        "month",
        "monthly",
        "period"
    },

    "unit_price": {
        "unit_price",
        "unit price",
        "price",
        "cost per unit",
        "item price"
    }
}


# =========================================================
# QUESTION INTENT KEYWORDS
# =========================================================

INTENT_KEYWORDS = {

    "ranking": {
        "highest",
        "lowest",
        "most",
        "least",
        "top",
        "bottom",
        "best",
        "worst",
        "maximum",
        "minimum"
    },

    "average": {
        "average",
        "avg",
        "mean"
    },

    "aggregation": {
        "total",
        "sum",
        "sales",
        "revenue",
        "amount",
        "income"
    },

    "count": {
        "count",
        "number",
        "how many",
        "frequency"
    },

    "trend": {
        "monthly",
        "month",
        "yearly",
        "year",
        "quarterly",
        "quarter",
        "over time",
        "trend",
        "growth"
    },

    "grouping": {
        "by",
        "per",
        "each"
    }
}


# =========================================================
# TEXT NORMALIZATION
# =========================================================

def normalize_text(
    text: str
) -> set[str]:
    """
    Convert text into normalized words.
    """

    text = str(
        text
    ).lower()

    text = text.replace(
        "_",
        " "
    )

    return set(
        re.findall(
            r"\b\w+\b",
            text
        )
    )


# =========================================================
# DETECT QUESTION INTENT
# =========================================================

def detect_question_intents(
    user_question: str
) -> set[str]:
    """
    Detect analytical intents from the user's question.
    """

    question_words = normalize_text(
        user_question
    )

    detected_intents = set()

    for intent, keywords in INTENT_KEYWORDS.items():

        for keyword in keywords:

            keyword_words = normalize_text(
                keyword
            )

            if keyword_words.issubset(
                question_words
            ):

                detected_intents.add(
                    intent
                )

                break

    return detected_intents


# =========================================================
# COLUMN SCORE
# =========================================================

def get_column_score(
    user_question: str,
    column: dict
) -> int:
    """
    Calculate how strongly a column is related
    to the user's question.
    """

    question_words = normalize_text(
        user_question
    )

    column_name = column["name"]

    score = 0


    # -----------------------------------------------------
    # DIRECT COLUMN NAME MATCH
    # -----------------------------------------------------

    column_words = normalize_text(
        column_name
    )

    if column_words.issubset(
        question_words
    ):

        score += 8

    elif question_words.intersection(
        column_words
    ):

        score += 3


    # -----------------------------------------------------
    # BUSINESS SYNONYM MATCH
    # -----------------------------------------------------

    if column_name in BUSINESS_SYNONYMS:

        for synonym in BUSINESS_SYNONYMS[
            column_name
        ]:

            synonym_words = normalize_text(
                synonym
            )

            if synonym_words.issubset(
                question_words
            ):

                score += 6

            elif question_words.intersection(
                synonym_words
            ):

                score += 2


    # -----------------------------------------------------
    # DESCRIPTION MATCH
    # -----------------------------------------------------

    description = column.get(
        "description",
        ""
    )

    description_words = normalize_text(
        description
    )

    description_matches = (
        question_words.intersection(
            description_words
        )
    )

    score += len(
        description_matches
    )


    # -----------------------------------------------------
    # RELATED CONCEPT MATCH
    # -----------------------------------------------------

    related_concepts = column.get(
        "related_concepts",
        []
    )

    for concept in related_concepts:

        concept_words = normalize_text(
            concept
        )

        if concept_words.issubset(
            question_words
        ):

            score += 6

        elif question_words.intersection(
            concept_words
        ):

            score += 2


    # -----------------------------------------------------
    # CUSTOMER ID / NAME PENALTY
    # -----------------------------------------------------

    if column_name in {
        "customer_id",
        "customer_name"
    }:

        if "customer" in question_words:

            score -= 5


    return score


# =========================================================
# FIND RELEVANT MEASURE FOR RANKING
# =========================================================

def find_ranking_measure(
    user_question: str,
    columns: list[dict]
) -> str | None:
    """
    Find the measure column used for a ranking question.

    Examples:

    revenue -> total_amount
    sales   -> total_amount
    units   -> quantity
    price   -> unit_price
    rating  -> rating
    """

    question_words = normalize_text(
        user_question
    )


    # -----------------------------------------------------
    # Score only analytical measures
    # -----------------------------------------------------

    measure_candidates = []

    for column in columns:

        if column["role"] != "measure":
            continue

        score = 0

        column_name = column["name"]


        # Direct column name
        column_words = normalize_text(
            column_name
        )

        if column_words.issubset(
            question_words
        ):

            score += 10


        # Business synonyms
        for synonym in BUSINESS_SYNONYMS.get(
            column_name,
            set()
        ):

            synonym_words = normalize_text(
                synonym
            )

            if synonym_words.issubset(
                question_words
            ):

                score += 10

            elif question_words.intersection(
                synonym_words
            ):

                score += 3


        # Related concepts
        for concept in column.get(
            "related_concepts",
            []
        ):

            concept_words = normalize_text(
                concept
            )

            if concept_words.issubset(
                question_words
            ):

                score += 8

            elif question_words.intersection(
                concept_words
            ):

                score += 2


        if score > 0:

            measure_candidates.append(
                (
                    column_name,
                    score
                )
            )


    if not measure_candidates:

        return None


    measure_candidates.sort(
        key=lambda item: item[1],
        reverse=True
    )


    return measure_candidates[0][0]


# =========================================================
# FIND RELEVANT DIMENSION FOR RANKING
# =========================================================

def find_ranking_dimension(
    user_question: str,
    columns: list[dict]
) -> str | None:
    """
    Find the categorical dimension used in
    a ranking question.

    Examples:

    city     -> city
    product  -> product
    category -> category
    """

    dimension_candidates = []

    for column in columns:

        if column["role"] not in {
            "categorical_dimension",
            "text_attribute"
        }:

            continue


        score = get_column_score(
            user_question,
            column
        )


        if score > 0:

            dimension_candidates.append(
                (
                    column["name"],
                    score
                )
            )


    if not dimension_candidates:

        return None


    dimension_candidates.sort(
        key=lambda item: item[1],
        reverse=True
    )


    return dimension_candidates[0][0]


# =========================================================
# RETRIEVE RELEVANT COLUMNS
# =========================================================

def retrieve_relevant_columns(
    user_question: str,
    columns: list[dict]
) -> list[str]:
    """
    Retrieve relevant columns using:

    1. Direct column names
    2. Business synonyms
    3. Semantic descriptions
    4. Related concepts
    5. Question intent
    6. Ranking-specific dimension + measure detection
    """

    if not user_question.strip():

        return []


    # -----------------------------------------------------
    # DETECT INTENTS
    # -----------------------------------------------------

    intents = detect_question_intents(
        user_question
    )


    # =====================================================
    # SPECIAL HANDLING FOR RANKING QUESTIONS
    # =====================================================

    if "ranking" in intents:

        dimension = find_ranking_dimension(
            user_question,
            columns
        )

        measure = find_ranking_measure(
            user_question,
            columns
        )


        ranking_columns = []


        if dimension is not None:

            ranking_columns.append(
                dimension
            )


        if measure is not None:

            ranking_columns.append(
                measure
            )


        if ranking_columns:

            return list(
                dict.fromkeys(
                    ranking_columns
                )
            )


    # =====================================================
    # NORMAL SEMANTIC RETRIEVAL
    # =====================================================

    scored_columns = []


    for column in columns:

        score = get_column_score(
            user_question,
            column
        )

        if score > 0:

            scored_columns.append(
                (
                    column["name"],
                    score
                )
            )


    if not scored_columns:

        return []


    # -----------------------------------------------------
    # SORT BY SCORE
    # -----------------------------------------------------

    scored_columns.sort(
        key=lambda item: item[1],
        reverse=True
    )


    best_score = (
        scored_columns[0][1]
    )


    # -----------------------------------------------------
    # RELEVANCE SETTINGS
    # -----------------------------------------------------

    MIN_SCORE = 5

    SCORE_MARGIN = 2


    # -----------------------------------------------------
    # SELECT STRONG MATCHES
    # -----------------------------------------------------

    relevant_columns = []

    for column_name, score in scored_columns:

        if score < MIN_SCORE:
            continue

        if (
            best_score - score
            <= SCORE_MARGIN
        ):

            relevant_columns.append(
                column_name
            )


    # -----------------------------------------------------
    # REMOVE DUPLICATES
    # -----------------------------------------------------

    relevant_columns = list(
        dict.fromkeys(
            relevant_columns
        )
    )


    return relevant_columns