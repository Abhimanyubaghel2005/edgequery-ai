import pandas as pd

from ai.gemini_sql import client


# ============================================================
# CLEAN TEXT
# ============================================================

def clean_insight(text: str) -> str:
    """
    Clean the text returned by Gemini.
    """

    if text is None:
        raise ValueError(
            "Gemini returned no business insight."
        )

    text = text.strip()

    if not text:
        raise ValueError(
            "Gemini returned an empty business insight."
        )

    return text


# ============================================================
# CONVERT RESULT TO TEXT
# ============================================================

def dataframe_to_text(
    df: pd.DataFrame
) -> str:
    """
    Convert the SQL result into a compact text
    representation for Gemini.
    """

    if df is None or df.empty:

        return "The SQL query returned no data."


    # Convert dataframe to a readable table.
    result_text = df.to_string(
        index=False
    )

    return result_text


# ============================================================
# GENERATE BUSINESS INSIGHT
# ============================================================

def generate_business_insight(
    user_question: str,
    result: pd.DataFrame
) -> str:
    """
    Generate a business-oriented insight from
    the user's question and SQL result.
    """

    # --------------------------------------------------------
    # VALIDATE QUESTION
    # --------------------------------------------------------

    if not user_question:

        raise ValueError(
            "User question cannot be empty."
        )


    # --------------------------------------------------------
    # CONVERT RESULT
    # --------------------------------------------------------

    result_text = dataframe_to_text(
        result
    )


    # --------------------------------------------------------
    # GEMINI PROMPT
    # --------------------------------------------------------

    prompt = f"""
You are a Business Intelligence analyst.

Analyze the SQL query result and provide
a concise, useful business insight.

USER QUESTION:
{user_question}

SQL RESULT:
{result_text}

RULES:

1. Use ONLY the information available in the SQL result.
2. Do not invent facts.
3. Do not assume information that is not present.
4. Do not mention that you are an AI.
5. Do not repeat the entire table.
6. Identify the most important business finding.
7. Include numbers when they are available.
8. Explain the finding in simple business language.
9. Keep the response concise.
10. Maximum 3 short paragraphs.
11. If the result contains rankings, identify the highest
    and lowest values when meaningful.
12. If the result contains percentages, explain the
    contribution or share.
13. If the result contains a time trend, explain the
    important increase, decrease, peak or low point.
14. Do not provide recommendations unless the data
    clearly supports them.

Write the business insight now.
"""


    # --------------------------------------------------------
    # CALL GEMINI
    # --------------------------------------------------------

    response = client.models.generate_content(

        model="gemini-3.5-flash-lite",

        contents=prompt

    )


    # --------------------------------------------------------
    # EXTRACT RESPONSE
    # --------------------------------------------------------

    insight = response.text


    # --------------------------------------------------------
    # CLEAN RESPONSE
    # --------------------------------------------------------

    insight = clean_insight(
        insight
    )


    return insight