import streamlit as st
import pandas as pd


# =========================================================
# DATA INGESTION
# =========================================================

from ingestion.loader import load_dataset


# =========================================================
# DATABASE
# =========================================================

from database.engine import (
    create_database,
    load_dataframe_to_database,
    execute_query
)


# =========================================================
# SCHEMA PROFILER
# =========================================================

from schema.profiler import profile_dataframe


# =========================================================
# SCHEMA CONTEXT
# =========================================================

from schema.context import (
    build_schema_context,
    build_relevant_schema_context
)


# =========================================================
# SCHEMA RETRIEVER
# =========================================================

from schema.retriever import (
    retrieve_relevant_columns
)


# =========================================================
# GEMINI TEXT-TO-SQL
# =========================================================

from ai.gemini_sql import generate_sql


# =========================================================
# SQL VALIDATION
# =========================================================

from sql.validator import (
    validate_sql,
    validate_column_references
)


# =========================================================
# VISUALIZATION
# =========================================================

from visualization.chart_generator import (
    generate_chart
)


# =========================================================
# BUSINESS INSIGHTS
# =========================================================

from insights.insight_generator import (
    generate_business_insight
)


# =========================================================
# STREAMLIT PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Text-to-SQL BI Engine",
    page_icon="🤖",
    layout="wide"
)


# =========================================================
# APPLICATION TITLE
# =========================================================

st.title(
    "🤖 AI-Powered Text-to-SQL & Automated BI Engine"
)

st.write(
    "Upload a structured dataset and ask questions "
    "using natural language."
)


# =========================================================
# DATASET UPLOADER
# =========================================================

uploaded_file = st.file_uploader(
    "Upload your dataset",
    type=[
        "csv",
        "xlsx",
        "json",
        "jsonl",
        "parquet"
    ]
)


# =========================================================
# MAIN APPLICATION
# =========================================================

if uploaded_file is not None:

    try:

        # =================================================
        # LOAD DATASET
        # =================================================

        df = load_dataset(
            uploaded_file
        )


        st.success(
            f"Dataset loaded successfully: "
            f"{len(df)} rows × {len(df.columns)} columns"
        )


        # =================================================
        # CREATE DATABASE
        # =================================================

        connection = create_database()


        load_dataframe_to_database(
            df,
            connection
        )


        # =================================================
        # DATASET PREVIEW
        # =================================================

        st.subheader(
            "📊 Dataset Preview"
        )


        st.dataframe(
            df.head(10),
            use_container_width=True
        )


        # =================================================
        # DATASET METRICS
        # =================================================

        metric1, metric2, metric3 = st.columns(3)


        with metric1:

            st.metric(
                "Rows",
                len(df)
            )


        with metric2:

            st.metric(
                "Columns",
                len(df.columns)
            )


        with metric3:

            st.metric(
                "Missing Values",
                int(
                    df.isnull().sum().sum()
                )
            )


        # =================================================
        # PROFILE DATASET
        # =================================================

        profile = profile_dataframe(
            df
        )


        # =================================================
        # COLUMN INFORMATION
        # =================================================

        st.subheader(
            "📋 Column Information"
        )


        column_information = pd.DataFrame(
            {

                "Column": [
                    column["name"]
                    for column in profile["columns"]
                ],

                "Data Type": [
                    column["data_type"]
                    for column in profile["columns"]
                ],

                "Role": [
                    column["role"]
                    for column in profile["columns"]
                ],

                "Meaning": [
                    column["description"]
                    for column in profile["columns"]
                ],

                "Missing Values": [
                    column["missing_values"]
                    for column in profile["columns"]
                ],

                "Unique Values": [
                    column["unique_values"]
                    for column in profile["columns"]
                ]

            }
        )


        st.dataframe(
            column_information,
            use_container_width=True
        )


        # =================================================
        # FULL SCHEMA PROFILE
        # =================================================

        with st.expander(
            "🔍 View Full Schema Profile"
        ):

            st.json(
                profile
            )


        # =================================================
        # BUILD FULL SCHEMA CONTEXT
        # =================================================

        full_schema_context = build_schema_context(
            profile
        )


        # =================================================
        # VIEW FULL SCHEMA CONTEXT
        # =================================================

        with st.expander(
            "🧠 View Full Schema Context"
        ):

            st.code(
                full_schema_context,
                language="text"
            )


        # =================================================
        # NATURAL LANGUAGE QUESTION
        # =================================================

        st.subheader(
            "💬 Ask a Question About Your Data"
        )


        user_question = st.text_input(
            "Enter your question",
            placeholder=(
                "Example: Which product sold the most units?"
            )
        )


        # =================================================
        # GENERATE ANSWER BUTTON
        # =================================================

        if st.button(
            "🚀 Generate Answer"
        ):

            # =================================================
            # CHECK QUESTION
            # =================================================

            if not user_question.strip():

                st.warning(
                    "Please enter a question."
                )

            else:

                try:

                    # =========================================
                    # RETRIEVE RELEVANT COLUMNS
                    # =========================================

                    relevant_columns = (
                        retrieve_relevant_columns(
                            user_question,
                            profile["columns"]
                        )
                    )


                    # =========================================
                    # SHOW RETRIEVED COLUMNS
                    # =========================================

                    with st.expander(
                        "🔎 Retrieved Relevant Columns"
                    ):

                        if relevant_columns:

                            st.write(
                                relevant_columns
                            )

                        else:

                            st.info(
                                "No specific columns were "
                                "identified. The complete "
                                "schema will be used."
                            )


                    # =========================================
                    # BUILD RELEVANT SCHEMA CONTEXT
                    # =========================================

                    if relevant_columns:

                        schema_context = (
                            build_relevant_schema_context(
                                profile,
                                relevant_columns
                            )
                        )

                    else:

                        schema_context = (
                            build_schema_context(
                                profile
                            )
                        )


                    # =========================================
                    # SHOW SCHEMA SENT TO GEMINI
                    # =========================================

                    with st.expander(
                        "🧠 Schema Context Sent to Gemini"
                    ):

                        st.code(
                            schema_context,
                            language="text"
                        )


                    # =========================================
                    # GENERATE SQL
                    # =========================================

                    with st.spinner(
                        "Generating SQL..."
                    ):

                        sql_query = generate_sql(
                            user_question,
                            schema_context
                        )


                    # =========================================
                    # SHOW GENERATED SQL
                    # =========================================

                    st.subheader(
                        "📝 Generated SQL"
                    )


                    st.code(
                        sql_query,
                        language="sql"
                    )


                    # =========================================
                    # SECURITY + COLUMN VALIDATION
                    # =========================================

                    is_safe, validation_message = (
                        validate_column_references(
                            sql_query,
                            df.columns.tolist()
                        )
                    )


                    # =========================================
                    # REJECT UNSAFE SQL
                    # =========================================

                    if not is_safe:

                        st.error(
                            "SQL query rejected: "
                            f"{validation_message}"
                        )


                    else:

                        # =====================================
                        # VALIDATION SUCCESS
                        # =====================================

                        st.success(
                            "SQL query passed security "
                            "and schema validation."
                        )


                        # =====================================
                        # EXECUTE SQL
                        # =====================================

                        with st.spinner(
                            "Executing SQL..."
                        ):

                            result = execute_query(
                                sql_query,
                                connection
                            )


                        # =====================================
                        # QUERY RESULT
                        # =====================================

                        st.subheader(
                            "📊 Query Result"
                        )


                        if result.empty:

                            st.warning(
                                "The query returned no results."
                            )


                        else:

                            st.dataframe(
                                result,
                                use_container_width=True
                            )


                            # =================================
                            # AUTOMATIC VISUALIZATION
                            # =================================

                            st.subheader(
                                "📈 Automatic Visualization"
                            )


                            try:

                                chart = generate_chart(
                                    result,
                                    user_question
                                )


                                if chart is not None:

                                    st.plotly_chart(
                                        chart,
                                        use_container_width=True
                                    )

                                else:

                                    st.info(
                                        "No suitable visualization "
                                        "could be generated."
                                    )


                            except Exception as chart_error:

                                st.warning(
                                    "Visualization could not "
                                    "be generated: "
                                    f"{chart_error}"
                                )


                            # =================================
                            # BUSINESS INSIGHT
                            # =================================

                            st.subheader(
                                "🧠 Business Insight"
                            )


                            try:

                                with st.spinner(
                                    "Generating business insight..."
                                ):

                                    insight = (
                                        generate_business_insight(
                                            user_question,
                                            result
                                        )
                                    )


                                st.info(
                                    insight
                                )


                            except Exception as insight_error:

                                st.warning(
                                    "Business insight could not "
                                    "be generated: "
                                    f"{insight_error}"
                                )


                except Exception as error:

                    st.error(
                        "An error occurred while processing "
                        f"your question: {error}"
                    )


        # =================================================
        # SEPARATOR
        # =================================================

        st.divider()


        # =================================================
        # MANUAL SQL SECTION
        # =================================================

        st.subheader(
            "🛠️ Manual SQL Query"
        )


        st.write(
            "You can also execute a SELECT query manually."
        )


        manual_query = st.text_area(
            "Enter SQL query",
            placeholder=(
                "SELECT * FROM dataset LIMIT 10;"
            )
        )


        # =================================================
        # EXECUTE MANUAL SQL
        # =================================================

        if st.button(
            "▶️ Execute SQL"
        ):

            # =============================================
            # CHECK EMPTY QUERY
            # =============================================

            if not manual_query.strip():

                st.warning(
                    "Please enter a SQL query."
                )


            else:

                try:

                    # =====================================
                    # BASIC SQL VALIDATION
                    # =====================================

                    is_safe, validation_message = (
                        validate_sql(
                            manual_query
                        )
                    )


                    # =====================================
                    # REJECT UNSAFE SQL
                    # =====================================

                    if not is_safe:

                        st.error(
                            "SQL query rejected: "
                            f"{validation_message}"
                        )


                    else:

                        # =================================
                        # COLUMN VALIDATION
                        # =================================

                        columns_valid, column_message = (
                            validate_column_references(
                                manual_query,
                                df.columns.tolist()
                            )
                        )


                        if not columns_valid:

                            st.error(
                                "SQL query rejected: "
                                f"{column_message}"
                            )


                        else:

                            st.success(
                                "SQL query passed security "
                                "and schema validation."
                            )


                            # =============================
                            # EXECUTE MANUAL QUERY
                            # =============================

                            result = execute_query(
                                manual_query,
                                connection
                            )


                            # =============================
                            # QUERY RESULT
                            # =============================

                            st.subheader(
                                "📊 Query Result"
                            )


                            if result.empty:

                                st.warning(
                                    "The query returned no results."
                                )


                            else:

                                st.dataframe(
                                    result,
                                    use_container_width=True
                                )


                                # =============================
                                # VISUALIZATION
                                # =============================

                                st.subheader(
                                    "📈 Automatic Visualization"
                                )


                                try:

                                    chart = generate_chart(
                                        result
                                    )


                                    if chart is not None:

                                        st.plotly_chart(
                                            chart,
                                            use_container_width=True
                                        )

                                    else:

                                        st.info(
                                            "No suitable visualization "
                                            "could be generated."
                                        )


                                except Exception as chart_error:

                                    st.warning(
                                        "Visualization could not "
                                        "be generated: "
                                        f"{chart_error}"
                                    )


                except Exception as error:

                    st.error(
                        "An error occurred while executing "
                        f"the SQL query: {error}"
                    )


    # =====================================================
    # DATASET LOADING ERROR
    # =====================================================

    except Exception as error:

        st.error(
            "The dataset could not be loaded: "
            f"{error}"
        )


# =========================================================
# NO DATASET UPLOADED
# =========================================================

else:

    st.info(
        "Please upload a CSV, Excel, JSON, JSONL, "
        "or Parquet dataset to begin."
    )