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

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd llm-warehouse-assistant
   ```

2. **Set up a virtual environment:**
   ```bash
   python3.12 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Create a `.env` file in the root directory and add your Groq API key:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

5. **Run dbt transformations (Optional/If applicable):**
   ```bash
   dbt run
   ```

6. **Launch the application:**
   ```bash
   python app.py
   ```

---

## 💡 Usage

Once the application is running, open the provided local URL (usually `http://127.0.0.1:7860`) in your browser. 

*   **Step 1:** Type a question in the text box (e.g., *"What was the total volume of documents processed last month?"*).
*   **Step 2:** Click **Submit**.
*   **Step 3:** View the generated SQL query, the raw data table, and the natural-language summary answer.
