# LLM Warehouse Assistant 🧠

A natural-language data assistant built with **Gradio**, **Groq**, **DuckDB**, and **dbt**.

Ask questions about your document warehouse in plain English. The application automatically generates SQL, executes it safely against DuckDB, and returns a clear, natural-language answer based on the retrieved data.

---

## 🚀 Features

*   **Natural-Language Interactivity:** Query your data warehouse without writing a single line of SQL.
*   **LLM-Powered SQL Generation:** Translates complex phrasing into precise SQL queries.
*   **Self-Healing SQL:** Automatically detects and corrects SQL syntax errors before execution.
*   **Modern Analytics Backend:** Powered by DuckDB for lightning-fast local OLAP queries and dbt for robust data transformations.
*   **Human-Readable Summaries:** Raw data tables are automatically synthesized into conversational insights.

---

## 🛠️ Tech Stack

*   **Language:** Python 3.12
*   **UI Framework:** Gradio
*   **LLM Provider:** Groq API
*   **Database:** DuckDB
*   **Data Transformation:** dbt (Data Build Tool)
*   **Data Manipulation:** Pandas

---

## 📦 Installation & Setup

### Option A: Using `uv` (Recommended & Fastest)
You can run the application immediately without manually managing environments, or set up a standard workspace using `uv`.

**Single-command execution (using `pyproject.toml` or script inline metadata):**
```bash
git clone https://github.com
cd llm-warehouse-assistant
uv run app.py
```

**Standard workspace setup:**
```bash
uv venv --python 3.12
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

### Option B: Using standard `pip`
```bash
git clone https://github.com
cd llm-warehouse-assistant
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## ⚙️ Configuration & Execution

1. **Configure environment variables:**
   Create a `.env` file in the root directory and add your Groq API key:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

2. **Run dbt transformations (Optional/If applicable):**
   ```bash
   # If using uv workspace or standard pip:
   dbt run

   # If using uv tool execution:
   uv run dbt run
   ```

3. **Launch the application:**
   ```bash
   python app.py
   ```

---

## 💡 Usage

Once the application is running, open the provided local URL (usually `http://127.0.0.1:7860`) in your browser. 

*   **Step 1:** Type a question in the text box (e.g., *"What was the total volume of documents processed last month?"*).
*   **Step 2:** Click **Submit**.
*   **Step 3:** View the generated SQL query, the raw data table, and the natural-language summary answer.
