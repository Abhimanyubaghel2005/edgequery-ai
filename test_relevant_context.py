import pandas as pd

from schema.profiler import profile_dataframe
from schema.retriever import retrieve_relevant_columns
from schema.context import build_relevant_schema_context


# ============================================================
# LOAD DATASET
# ============================================================

df = pd.read_csv(
    "sample_customer_shopping_data.csv"
)


# ============================================================
# SHOW COLUMNS
# ============================================================

print("\nDATASET COLUMNS:")
print(df.columns.tolist())


# ============================================================
# CREATE PROFILE
# ============================================================

profile = profile_dataframe(df)


# ============================================================
# QUESTION
# ============================================================

question = "Which product sold the most units?"


print("\nQUESTION:")
print(question)


# ============================================================
# RETRIEVE COLUMNS
# ============================================================

relevant_columns = retrieve_relevant_columns(
    question,
    df.columns.tolist()
)


print("\nRELEVANT COLUMNS:")
print(relevant_columns)


# ============================================================
# BUILD RELEVANT CONTEXT
# ============================================================

context = build_relevant_schema_context(
    profile,
    relevant_columns
)


print("\n========================================")
print("RELEVANT SCHEMA CONTEXT")
print("========================================")

print(context)

print("========================================")