import pandas as pd

from schema.profiler import profile_dataframe

from schema.retriever import (
    retrieve_relevant_columns
)


# =========================================================
# LOAD DATASET
# =========================================================

df = pd.read_csv(
    "sample_customer_shopping_data.csv"
)


# =========================================================
# CREATE SCHEMA PROFILE
# =========================================================

profile = profile_dataframe(
    df
)


# =========================================================
# TEST QUESTIONS
# =========================================================

questions = [

    "Which city generated the highest revenue?",

    "Which product sold the most units?",

    "What is the average customer age?",

    "Show monthly sales.",

    "Which category has the highest revenue?",

    "What is the average price?"
]


# =========================================================
# TEST RETRIEVER
# =========================================================

for question in questions:

    result = retrieve_relevant_columns(
        question,
        profile["columns"]
    )

    print(
        f"\nQuestion: {question}"
    )

    print(
        f"Relevant columns: {result}"
    )