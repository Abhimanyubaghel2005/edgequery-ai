from sql.validator import validate_sql


# --------------------------------------------------
# TEST 1: SAFE SQL
# --------------------------------------------------

safe_sql = "SELECT AVG(salary) FROM dataset;"

print("========== SAFE SQL TEST ==========")
print("SQL:")
print(safe_sql)

is_safe, message = validate_sql(safe_sql)

print("\nIs Safe:", is_safe)
print("Message:", message)


# --------------------------------------------------
# TEST 2: UNSAFE SQL
# --------------------------------------------------

unsafe_sql = "DROP TABLE dataset;"

print("\n========== UNSAFE SQL TEST ==========")
print("SQL:")
print(unsafe_sql)

is_safe, message = validate_sql(unsafe_sql)

print("\nIs Safe:", is_safe)
print("Message:", message)