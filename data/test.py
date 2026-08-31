import duckdb

# Connect to your database
con = duckdb.connect("data/warehouse.duckdb")

# 1. List all tables
print("--- TABLES ---")
tables = con.sql("SHOW TABLES").fetchall()
for table in tables:
    print(table[0])

print("\n--- ROW COUNTS ---")
# 2. Get row count for each table
for table in tables:
    table_name = table[0]
    # Count rows in the table
    row_count = con.sql(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
    print(f"Table '{table_name}' has {row_count:,} rows")

# Close the connection
con.close()
