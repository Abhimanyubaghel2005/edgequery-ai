import pandas as pd

from schema.profiler import profile_dataframe
from schema.context import build_schema_context
from ai.gemini_sql import generate_sql


# Create test dataset
data = {
    "name": [
        "Amit",
        "Rahul",
        "Priya",
        "Neha"
    ],
    "age": [
        22,
        24,
        23,
        25
    ],
    "salary": [
        50000,
        60000,
        55000,
        70000
    ]
}


df = pd.DataFrame(data)


# Generate schema profile
profile = profile_dataframe(df)


# Generate schema context
schema_context = build_schema_context(
    profile,
    table_name="dataset"
)


# Ask a natural-language question
question = "What is the average salary?"


# Generate SQL
sql = generate_sql(
    question,
    schema_context
)


print("\nUser Question:")
print(question)

print("\nGenerated SQL:")
print(sql)
