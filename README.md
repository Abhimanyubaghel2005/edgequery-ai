
# EdgeQuery AI

## Intelligent Text-to-SQL & Business Intelligence Platform

EdgeQuery AI is an AI-powered Business Intelligence platform that allows users to upload structured datasets and ask questions about their data using natural language.

Instead of manually writing SQL queries, users can ask questions such as:

> Which city generated the highest revenue?

EdgeQuery AI analyzes the dataset, identifies the relevant schema, generates SQL using Google Gemini, validates the query using SQLGlot, executes it against SQLite, and presents the result with an automatic visualization and business insight.

---

## 🚀 How It Works

```text
User uploads dataset
        ↓
Data ingestion
        ↓
Schema profiling
        ↓
Relevant schema retrieval
        ↓
User asks a question
        ↓
Google Gemini generates SQL
        ↓
SQLGlot validates the SQL
        ↓
SQLite executes the query
        ↓
Query result
        ↓
Automatic visualization
        ↓
Business insight
````

---

## ✨ Key Features

### 📂 Multiple Dataset Formats

EdgeQuery AI supports:

* CSV
* Excel / XLSX
* JSON
* JSONL
* Parquet

### 🔍 Automatic Schema Profiling

The system automatically analyzes the uploaded dataset and identifies:

* Column names
* Data types
* Missing values
* Unique values
* Sample values
* Numeric ranges
* Column roles
* Business concepts

### 🧠 Semantic Schema Retrieval

Instead of sending the complete dataset schema to the AI model, EdgeQuery retrieves the columns most relevant to the user's question.

For example:

**Question:**

```text
Which city generated the highest revenue?
```

Relevant columns:

```text
city
total_amount
```

### 🤖 AI-Powered Text-to-SQL

Google Gemini converts natural-language questions into SQLite-compatible SQL.

Example:

**Question:**

```text
Which product sold the most units?
```

**Generated SQL:**

```sql
SELECT
    product,
    SUM(quantity) AS total_units
FROM dataset
GROUP BY product
ORDER BY total_units DESC
LIMIT 1;
```

### 🔐 SQL Security Validation

Generated SQL is validated before execution using SQLGlot.

The system blocks destructive operations such as:

```text
INSERT
UPDATE
DELETE
DROP
CREATE
ALTER
```

Only read-oriented SQL queries are allowed.

### 🧩 Schema-Aware Validation

The system also checks whether the generated SQL references columns that actually exist in the uploaded dataset.

For example, if the dataset does not contain:

```text
revenue
```

then:

```sql
SELECT revenue FROM dataset;
```

will be rejected.

### 📊 Automatic Visualization

After executing the SQL query, EdgeQuery automatically selects an appropriate visualization using Plotly.

Supported visualization types include:

* Bar charts
* Line charts
* Donut charts
* Histograms
* Scatter plots
* Box plots

### 💡 Business Insights

The query result is passed to Gemini to generate a concise business-oriented insight based only on the available result.

---

# 🏗️ Architecture

```text
                    User
                     │
                     ▼
              Dataset Upload
                     │
                     ▼
             Data Ingestion
                     │
                     ▼
             Schema Profiler
                     │
                     ▼
          Schema Retrieval Layer
                     │
                     ▼
             User Question
                     │
                     ▼
              Google Gemini
              Text → SQL
                     │
                     ▼
            SQLGlot Validation
           ┌─────────┴─────────┐
           │                   │
      Security Check      Column Check
           │                   │
           └─────────┬─────────┘
                     ▼
              SQLite Database
                     │
                     ▼
               Query Result
                /        \
               /          \
              ▼            ▼
       Visualization    AI Insight
              \            /
               \          /
                ▼        ▼
                 Streamlit
                     │
                     ▼
                    User
```

---

# 🛠️ Tech Stack

| Technology        | Purpose                           |
| ----------------- | --------------------------------- |
| Python            | Core development                  |
| Streamlit         | Web application interface         |
| Pandas            | Data processing                   |
| SQLite            | SQL execution                     |
| Google Gemini API | Text-to-SQL and business insights |
| SQLGlot           | SQL parsing and validation        |
| Plotly            | Data visualization                |
| Docker            | Containerization                  |
| Git               | Version control                   |
| GitHub            | Source code management            |
| Render            | Deployment                        |

---

# 📁 Project Structure

```text
edgequery-ai/
│
├── ai/
│   ├── __init__.py
│   └── gemini_sql.py
│
├── database/
│   ├── __init__.py
│   └── engine.py
│
├── ingestion/
│   ├── __init__.py
│   └── loader.py
│
├── insights/
│   ├── __init__.py
│   └── insight_generator.py
│
├── schema/
│   ├── __init__.py
│   ├── context.py
│   ├── profiler.py
│   └── retriever.py
│
├── sql/
│   ├── __init__.py
│   └── validator.py
│
├── visualization/
│   ├── __init__.py
│   └── chart_generator.py
│
├── tests/
│   ├── test_context.py
│   ├── test_database.py
│   ├── test_gemini.py
│   ├── test_gemini_sql.py
│   ├── test_insights.py
│   ├── test_relevant_context.py
│   ├── test_retriever.py
│   ├── test_schema.py
│   ├── test_sql_security.py
│   ├── test_validator.py
│   └── test_visualization.py
│
├── app.py
├── sample_customer_shopping_data.csv
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── README.md
└── requirements.txt
```

---

# 💻 Installation

## 1. Clone the repository

```bash
git clone https://github.com/Abhimanyubaghel2005/edgequery-ai.git
```

```bash
cd edgequery-ai
```

## 2. Create a virtual environment

### Windows

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

## 3. Install dependencies

```powershell
pip install -r requirements.txt
```

---

# 🔑 Environment Configuration

Create a `.env` file in the project root.

Add:

```text
GEMINI_API_KEY=your_actual_gemini_api_key
```

You can use `.env.example` as a template.

**Never commit your real API key to GitHub.**

The `.env` file is excluded through `.gitignore`.

---

# ▶️ Run Locally

Start the Streamlit application:

```powershell
streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

---

# 🐳 Run with Docker

EdgeQuery AI is containerized using Docker.

## Build the image

```powershell
docker build -t edgequery-ai .
```

## Run the container

```powershell
docker run -d --name edgequery-ai-container -p 8501:8501 --env-file .env edgequery-ai
```

Open:

```text
http://localhost:8501
```

---

# 🧪 Example Questions

Using the included customer shopping dataset, you can ask:

### Revenue

```text
Which city generated the highest revenue?
```

### Product Performance

```text
Which product sold the most units?
```

### Customer Analysis

```text
What is the average customer age?
```

### Monthly Sales

```text
Show monthly sales.
```

### Category Performance

```text
Which category has the highest revenue?
```

### Pricing

```text
What is the average price?
```

---

# 📊 Sample Dataset

The repository contains:

```text
sample_customer_shopping_data.csv
```

Example columns include:

```text
customer_id
customer_name
city
age
category
product
quantity
unit_price
rating
purchase_month
total_amount
```

---

# 🔒 Security

EdgeQuery does not execute AI-generated SQL directly.

The query passes through a validation pipeline:

```text
Gemini-generated SQL
        ↓
SQLGlot parser
        ↓
Statement validation
        ↓
Column validation
        ↓
SQLite execution
```

The validation layer helps prevent:

* Destructive SQL operations
* Multiple SQL statements
* Invalid SQL syntax
* Unknown dataset columns

API credentials are stored through environment variables and are not included in the repository.

---

# 🧪 Testing

The project contains tests for important components including:

* Database operations
* Schema profiling
* Schema context
* Schema retrieval
* SQL validation
* SQL security
* Gemini SQL generation
* Visualization
* Business insights

All test files are organized inside:

```text
tests/
```

---

# 🚀 Deployment

The application is Dockerized and can be deployed to cloud platforms that support Docker-based applications.

Current deployment platform:

**Render**

Live Demo:

```text
Add your Render URL here
```

---

# ⚠️ Current Limitations

The current version is designed primarily for structured and tabular datasets.

Supported formats:

```text
CSV
Excel
JSON
JSONL
Parquet
```

The current SQL execution layer uses SQLite and a single logical table named:

```text
dataset
```

Advanced capabilities such as multi-table JOINs, PostgreSQL support, authentication, query history, and advanced production monitoring are planned for future versions.

---

# 🗺️ Roadmap

## V1

* [x] Generic dataset ingestion
* [x] CSV support
* [x] Excel support
* [x] JSON support
* [x] JSONL support
* [x] Parquet support
* [x] Schema profiling
* [x] Schema retrieval
* [x] Gemini Text-to-SQL
* [x] SQL security validation
* [x] Schema-aware validation
* [x] SQLite execution
* [x] Automatic visualization
* [x] Business insights
* [x] Streamlit UI
* [x] Dockerization
* [x] GitHub repository
* [x] Deployment

## V2

* [ ] Evidence Engine
* [ ] Reproducible answer IDs
* [ ] Multi-table JOIN support
* [ ] PostgreSQL support
* [ ] Query history
* [ ] Authentication
* [ ] SQL self-correction
* [ ] Advanced dashboards
* [ ] Production monitoring

---

# 🔎 Future: Evidence Engine

A planned V2 capability is the **EdgeQuery Evidence Engine**.

The goal is to make AI-generated business answers more transparent by showing the chain behind an answer:

```text
User Question
      ↓
Relevant Schema
      ↓
Generated SQL
      ↓
SQL Validation
      ↓
Query Execution
      ↓
Result Evidence
      ↓
Visualization
      ↓
Business Insight
```

This will help users understand how an AI-generated answer was produced and provide a reproducible analytical workflow.

---

# 👨‍💻 Author

**Abhimanyu Singh**

B.Tech — Electronics & Communication Engineering

### Areas of Interest

* Data Analytics
* Business Intelligence
* Artificial Intelligence
* Software Engineering
* Python
* SQL
* Machine Learning
* Data Engineering

### GitHub

[https://github.com/Abhimanyubaghel2005](https://github.com/Abhimanyubaghel2005)


