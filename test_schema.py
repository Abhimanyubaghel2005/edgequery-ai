import pandas as pd

from schema.profiler import profile_dataframe


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


print("\nSchema Profile:")
print(profile)