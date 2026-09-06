import os
import duckdb
import re
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

MODEL = "openai/gpt-oss-120b"
TEMPERATURE = 0.1
DB_PATH = "data/warehouse.duckdb"
TABLE_NAME = "fct_documents"
MAX_RETRIES = 2

def get_warehouse_schema(db_path: str = DB_PATH) -> str:
    """Extracts schema layout definitions from your production mart."""
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found at: {db_path}.")
        
    conn = duckdb.connect(db_path)
    try:
        schema_df = conn.execute(f"DESCRIBE {TABLE_NAME};").fetchdf()
        return schema_df.to_string()
    except Exception as e:
        raise RuntimeError(f"Failed to extract database context: {e}")
    finally:
        conn.close()

def execute_sql(sql_query: str, db_path: str = DB_PATH) -> tuple[bool, str]:
    """Executes a generated SQL query safely against DuckDB."""
    conn = duckdb.connect(db_path)
    try:
        res = conn.execute(sql_query).fetchdf()
        return True, res.to_string()
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def extract_content(choice_obj) -> str:
    """Safely extracts content payload from response objects."""
    raw_str = str(choice_obj)
    match = re.search(r"content=['\"](.*?)['\"], role=", raw_str, re.DOTALL)
    if match:
        return match.group(1).encode().decode('unicode-escape')
    if isinstance(choice_obj, list) and len(choice_obj) > 0:
        choice_obj = choice_obj[0]
    if hasattr(choice_obj, "message") and hasattr(choice_obj.message, "content"):
        return choice_obj.message.content
    if isinstance(choice_obj, dict) and "message" in choice_obj:
        return choice_obj["message"].get("content", "")
    return raw_str

def process_user_query(user_input: str) -> tuple[str, str, str]:
    """
    Processes user input and returns:
    (generated_sql, raw_query_result, final_natural_language_answer)
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Missing GROQ_API_KEY environment variable.")

    db_schema = get_warehouse_schema()
    client = Groq(api_key=api_key)

    system_prompt = (
        "You are an expert data analyst assistant linked directly to a local DuckDB warehouse engine layer.\n"
        f"Your active target table is named: {TABLE_NAME}\n"
        f"Here is the database schema definition:\n{db_schema}\n\n"
        "CRITICAL: When asked a question, respond ONLY with a raw valid SQL query that answers it. "
        "Do not include markdown code block formatting, backticks, or preamble text. Just output raw executable SQL code."
    )

    messages_history = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]

    success = False
    query_result = ""
    generated_sql = ""

    # Self-healing SQL generation loop
    for attempt in range(MAX_RETRIES + 1):
        completion = client.chat.completions.create(
            model=MODEL,
            messages=messages_history,
            temperature=TEMPERATURE
        )
        
        generated_sql = extract_content(completion.choices)
        generated_sql = generated_sql.replace("```sql", "").replace("```", "").strip()
        
        success, query_result = execute_sql(generated_sql)
        if success:
            break
            
        if attempt < MAX_RETRIES:
            messages_history.append({"role": "assistant", "content": generated_sql})
            messages_history.append({
                "role": "user", 
                "content": f"That query failed with error: {query_result}. Correct the SQL and output raw SQL code only."
            })

    if not success:
        return generated_sql, query_result, f"❌ Unable to execute valid SQL after retries. Error: {query_result}"

    # Natural Language Interpretation
    interpretation = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Summarize the raw database output values to answer the user's question clearly using clean markdown."},
            {"role": "user", "content": f"User question: {user_input}\nExecuted SQL: {generated_sql}\nRaw Query Result:\n{query_result}"}
        ],
        temperature=TEMPERATURE
    )
    
    final_answer = extract_content(interpretation.choices)
    return generated_sql, query_result, final_answer