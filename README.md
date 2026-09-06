# LLM Warehouse Assistant 🧠

A natural-language data assistant built with **Gradio**, **Groq**, **DuckDB**, and **dbt**.

Ask questions about your document warehouse in plain English. The application uses an LLM to generate SQL, executes the SQL against DuckDB, and converts the results into a clear natural-language answer.

---

## 🎓 Course Project Context

This project was developed as an official academic assignment for the PGD **Generative AI Course** at **NED University of Engineering and Technology**.

* **Supervised By:** [Sir Sajid Majeed](https://github.com/SajidMajeed92)
* **Project Team:**
  * [Bilal Mansoor](https://github.com/mbilalmansoor)

---

## 🚀 Features

*   **Natural-Language Queries** — Ask questions about your warehouse without writing SQL.
*   **LLM-Powered SQL Generation** — Converts natural-language questions into SQL queries.
*   **Self-Healing SQL** — Automatically retries failed SQL queries and asks the LLM to correct them.
*   **DuckDB Warehouse** — Uses DuckDB as the local analytical database.
*   **dbt Transformations** — Transforms raw documents into the `fct_documents` analytical table.
*   **Natural-Language Answers** — Converts database results into readable explanations.
*   **Gradio Interface** — Provides a simple web interface for interacting with the warehouse.

---

## 🛠️ Tech Stack

<p align="left">
  <a href="https://python.org" target="_blank" rel="noreferrer"><img src="https://githubusercontent.com" alt="Python" width="36" height="36" /></a>
  <a href="https://github.com" target="_blank" rel="noreferrer"><img src="https://githubusercontent.com" alt="uv" width="36" height="36" style="border-radius: 4px;" /></a>
  <a href="https://gradio.app" target="_blank" rel="noreferrer"><img src="https://githubusercontent.com" alt="Gradio" width="36" height="36" /></a>
  <a href="https://groq.com" target="_blank" rel="noreferrer"><img src="https://seeklogo.com" alt="Groq" width="45" height="36" style="object-fit: contain;" /></a>
  <a href="https://duckdb.org" target="_blank" rel="noreferrer"><img src="https://duckdb.orgimages/favicon/apple-touch-icon.png" alt="DuckDB" width="36" height="36" /></a>
  <a href="https://getdbt.com" target="_blank" rel="noreferrer"><img src="https://seeklogo.com" alt="dbt" width="36" height="36" /></a>
  <a href="https://pydata.org" target="_blank" rel="noreferrer"><img src="https://githubusercontent.com" alt="Pandas" width="36" height="36" /></a>
</p>

*   **Python:** 3.12+
*   **Package Manager:** uv
*   **UI:** Gradio
*   **LLM:** Groq API
*   **Database:** DuckDB
*   **Data Transformation:** dbt
*   **Data Processing:** Pandas

---

## 📁 Project Structure

```text
LLM_Wareshouse/
├── app.py
├── data/
│   └── data.csv
├── dbt_models/
│   ├── fct_documents.sql
│   └── sources.yml
├── src/
│   ├── db_ingest.py
│   └── llm_wareshouse/
│       ├── __init__.py
│       └── query.py
├── dbt_project.yml
├── profiles.yml
├── pyproject.toml
├── requirements.txt
└── uv.lock
```

### Main Components
*   `app.py` — Gradio web application.
*   `src/db_ingest.py` — Loads the CSV data into the DuckDB warehouse.
*   `src/llm_wareshouse/query.py` — Generates SQL with Groq, executes it against DuckDB, and produces the final answer.
*   `dbt_models/fct_documents.sql` — Creates the transformed `fct_documents` table.
*   `dbt_models/sources.yml` — Defines the raw DuckDB source.
*   `data/data.csv` — Source document dataset.
*   `dbt_project.yml` — dbt project configuration.
*   `profiles.yml` — DuckDB connection configuration.

---

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mbilalmansoor/LLM_Wareshouse.git
   cd LLM_Wareshouse
   ```

2. **Install dependencies with uv:**
   If you don't already have `uv` installed, install it first. Then run:
   ```bash
   uv sync
   ```
   This creates and manages the project's virtual environment using the dependencies defined in `pyproject.toml` and `uv.lock`.

---

## 🔑 Configuration

Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
```
> ⚠️ **Important:** Never commit your `.env` file or expose your API key publicly.

---

## 🗄️ Initialize the Warehouse

First, load the source CSV into DuckDB:
```bash
uv run python src/db_ingest.py
```

Then run the dbt transformation:
```bash
uv run dbt run
```
This creates the transformed `fct_documents` table in `data/warehouse.duckdb`.

---

## ▶️ Run the Application

Start the Gradio application with:
```bash
uv run python app.py
```

The application will be available at: [http://127.0.0.1:7860](http://127.0.0.1:7860)

---

## 💬 Example Questions

Once the application is running, you can ask questions such as:
*   *How many documents are there?*
*   *Show me the documents in the warehouse.*
*   *What are the different categories of documents?*

### Query Workflow
1. Receive the natural-language question.
2. Provide the warehouse schema to the LLM.
3. Generate a SQL query.
4. Execute the query against DuckDB.
5. Retry if the generated SQL fails.
6. Send the database result back to the LLM.
7. Return a natural-language answer.

---

## 🔄 Data Pipeline

```text
data/data.csv
      │
      ▼
src/db_ingest.py
      │
      ▼
   DuckDB
(raw_documents)
      │
      ▼
     dbt
      │
      ▼
fct_documents
      │
      ▼
src/llm_wareshouse/query.py
      │
      ├── Groq → SQL generation
      │
      ├── DuckDB → SQL execution
      │
      └── Groq → Natural-language answer
      │
      ▼
   app.py
      │
      ▼
  Gradio UI
```

---

## ⚠️ Notes

*   The DuckDB database is generated locally and should not be committed to Git.
*   dbt-generated files in `target/` should not be committed.
*   Logs and Python cache files should not be committed.
*   A valid `GROQ_API_KEY` is required to use the LLM functionality.

---

## 📄 License

This project is for educational and experimental purposes.
