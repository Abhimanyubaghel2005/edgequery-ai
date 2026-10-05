import pandas as pd

from database.engine import (
    create_database,
    load_dataframe_to_database,
    execute_query
)


data = {
    "name": [
        "Amit",
        "Rahul",
        "Priya",
        "Neha"
    ],
    "department": [
        "IT",
        "IT",
        "HR",
        "Finance"
    ],
    "salary": [
        50000,
        60000,
        55000,
        70000
    ]
}


df = pd.DataFrame(data)


connection = create_database()


load_dataframe_to_database(
    df,
    connection
)


query = """
SELECT
    department,
    AVG(salary) AS average_salary
FROM dataset
GROUP BY department
ORDER BY average_salary DESC;
"""


result = execute_query(
    query,
    connection
)


print("\nQuery Result:")
print(result)


connection.close()

print("\nTesting unsafe SQL:")

unsafe_query = "DROP TABLE dataset;"

try:

    execute_query(
        unsafe_query,
        connection
    )

except Exception as error:

    print("Blocked successfully:")
    print(error)