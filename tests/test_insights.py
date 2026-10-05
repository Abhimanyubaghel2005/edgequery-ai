import pandas as pd

from insights.insight_generator import (
    generate_business_insight
)


# ============================================================
# TEST DATA
# ============================================================

data = {

    "city": [
        "Pune",
        "Indore",
        "Mumbai",
        "Delhi",
        "Bhopal"
    ],

    "total_amount": [
        12900,
        19000,
        37000,
        49800,
        82600
    ]

}


result = pd.DataFrame(
    data
)


# ============================================================
# USER QUESTION
# ============================================================

question = (
    "What is the total amount by city?"
)


# ============================================================
# GENERATE BUSINESS INSIGHT
# ============================================================

print(
    "\nGenerating business insight..."
)


insight = generate_business_insight(
    question,
    result
)


# ============================================================
# DISPLAY RESULT
# ============================================================

print(
    "\n========================================"
)

print(
    "BUSINESS INSIGHT"
)

print(
    "========================================"
)

print(
    insight
)

print(
    "========================================"
)