import os
import duckdb

def raw_ingest(csv_path: str, db_path: str = "data/warehouse.duckdb", stage_table: str = "raw_documents"):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Source file not found at: {csv_path}")

    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    print(f"Connecting to DuckDB target storage layer: {db_path}")
    conn = duckdb.connect(db_path)
    
    try:
        # 1. Create the schema table blueprint ONLY if it does not exist yet
        conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {stage_table} AS 
            SELECT * FROM read_csv_auto('{csv_path}') LIMIT 0;
        """)
        
        # 2. Append new records straight down into the landing table block
        print(f"Appending raw dataset rows from '{csv_path}' into storage table '{stage_table}'...")
        conn.execute(f"""
            INSERT INTO {stage_table} 
            SELECT * FROM read_csv_auto('{csv_path}');
        """)
        
        row_count = conn.execute(f"SELECT COUNT(*) FROM {stage_table}").fetchone()[0]
        print(f"Successfully loaded records. Total rows now in raw staging table: {row_count}")
        
    except Exception as e:
        print(f"❌ Landing pass-through execution failed: {e}")
        raise e
    finally:
        conn.close()

if __name__ == "__main__":
    raw_ingest(csv_path="data/data.csv")
