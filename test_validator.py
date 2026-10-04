from sql.validator import validate_sql


test_queries = [

    "SELECT * FROM dataset;",

    "SELECT COUNT(*) FROM dataset;",

    "DROP TABLE dataset;",

    "DELETE FROM dataset;",

    "UPDATE dataset SET salary = 0;",

    "SELECT * FROM dataset; DROP TABLE dataset;"
]


for query in test_queries:

    is_safe, message = validate_sql(query)

    print("\nQuery:")
    print(query)

    print("Safe:", is_safe)

    print("Message:", message)