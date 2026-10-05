import pandas as pd

from schema.profiler import profile_dataframe
from schema.context import build_schema_context


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


profile = profile_dataframe(df)


context = build_schema_context(
    profile,
    table_name="dataset"
)


print("\nSchema Context:")
print(context)