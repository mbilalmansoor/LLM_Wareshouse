import os
import sys
import duckdb
import re
from dotenv import load_dotenv
from groq import Groq

# Load environment configuration keys from .env
load_dotenv()

# --- CONFIGURATION VARIABLES AT THE START ---
MODEL = "openai/gpt-oss-120b"
TEMPERATURE = 0.1
DB_PATH = "data/warehouse.duckdb"
TABLE_NAME = "fct_documents"
MAX_RETRIES = 2  # How many times the LLM can try to fix its own SQL error
# --------------------------------------------

def get_warehouse_schema(db_path: str = DB_PATH) -> str:
    """Extracts schema layout definitions from your production mart."""
    if not os.path.exists(db_path):
        print(f"❌ Database file not found at: {db_path}. Run ingestion and dbt first.")
        sys.exit(1)
        
    conn = duckdb.connect(db_path)
    try:
        schema_df = conn.execute(f"DESCRIBE {TABLE_NAME};").fetchdf()
        return schema_df.to_string()
    except Exception as e:
        print(f"❌ Failed to extract database context profile matrix: {e}")
        sys.exit(1)
    finally:
        conn.close()

def execute_sql(sql_query: str, db_path: str = DB_PATH) -> tuple[bool, str]:
    """Executes a generated SQL query safely against DuckDB. Returns (success_bool, result_str)."""
    conn = duckdb.connect(db_path)
    try:
        res = conn.execute(sql_query).fetchdf()
        return True, res.to_string()
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def extract_content(choice_obj) -> str:
    """Safely drills down into non-standard choice arrays to get the string payload."""
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

def interactive_warehouse_chat():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or "your_actual_key" in api_key:
        print("❌ Error: Missing real 'GROQ_API_KEY' setup definitions inside your root .env file.")
        return

    print("🔍 Inspecting production warehouse schema layers...")
    db_schema = get_warehouse_schema()
    
    client = Groq(api_key=api_key)
    
    # API & MODEL HEALTH CHECK 
    print(f"Test connection to Groq API and validating model '{MODEL}'...")
    try:
        client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=1
        )
        print("✅ Groq API connection and model verified successfully!")
    except Exception as e:
        print(f"❌ API/Model Validation Failed: {e}")
        sys.exit(1)

    system_prompt = (
        "You are an expert data analyst assistant linked directly to a local DuckDB warehouse engine layer.\n"
        f"Your active target table is named: {TABLE_NAME}\n"
        f"Here is the database schema definition:\n{db_schema}\n\n"
        "CRITICAL: When asked a question, respond ONLY with a raw valid SQL query that answers it. "
        "Do not include markdown code block formatting, backticks, or preamble text. Just output raw executable SQL code."
    )
    
    print(f"\n⚡ Groq SQL Agent Connected! (Using {MODEL})")
    print("💬 Ask anything about your total dataset data (Type 'exit' to quit)\n")
    
    while True:
        try:
            user_input = input("👤 You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ['exit', 'quit']:
                print("👋 Session closing down.")
                break
                
            # Initialize conversation messages array for potential self-healing loops
            messages_history = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
            
            success = False
            query_result = ""
            generated_sql = ""
            
            # --- SELF HEALING LOOP ---
            for attempt in range(MAX_RETRIES + 1):
                print(f"🤖 Generating optimized warehouse query (Attempt {attempt + 1})...")
                completion = client.chat.completions.create(
                    model=MODEL,
                    messages=messages_history,
                    temperature=TEMPERATURE
                )
                
                generated_sql = extract_content(completion.choices)
                generated_sql = generated_sql.replace("```sql", "").replace("```", "").strip()
                
                print(f"🖥️ Executing Query:\n{generated_sql}")
                success, query_result = execute_sql(generated_sql)
                
                if success:
                    break  # Query worked, break out of retry loop!
                    
                print(f"⚠️ SQL execution failed on attempt {attempt + 1}. Error: {query_result}")
                if attempt < MAX_RETRIES:
                    print("🔄 Sending error logs back to LLM to self-heal and regenerate...")
                    # Feed the broken SQL and the exact database error back to the LLM configuration history
                    messages_history.append({"role": "assistant", "content": generated_sql})
                    messages_history.append({
                        "role": "user", 
                        "content": f"That query failed with database error: {query_result}. Please fix the syntax or column names and provide the corrected raw SQL query."
                    })
            
            # If all retries fail completely, inform the user cleanly
            if not success:
                print(f"\n❌ Error: The model was unable to generate valid SQL after {MAX_RETRIES + 1} attempts.")
                print(f"Final error message: {query_result}\n" + "-"*50 + "\n")
                continue
            # ---------------------------
            
            # Let the LLM clean up and explain the true query result numbers back to the user
            interpretation = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": "Summarize the raw database output values to answer the user's question clearly. Format lists nicely using clean markdown bullet points or tables."},
                    {"role": "user", "content": f"User question: {user_input}\nExecuted SQL: {generated_sql}\nRaw Query Result Matrix Data:\n{query_result}"}
                ],
                temperature=TEMPERATURE
            )
            
            final_answer = extract_content(interpretation.choices)
            print(f"\n💡 Answer:\n{final_answer}\n" + "-"*50 + "\n")
            
        except KeyboardInterrupt:
            print("\n👋 Session closing down.")
            break
        except Exception as e:
            print(f"\n❌ Operational processing failure: {e}\n")

if __name__ == "__main__":
    interactive_warehouse_chat()
