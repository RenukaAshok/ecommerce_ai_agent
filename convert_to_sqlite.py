import pandas as pd
import sqlite3
import os

# Folder where your data is stored
DATA_FOLDER = 'data'
# Name of the database file to be created
DB_NAME = 'ecommerce.db'

# Create a connection to the SQLite database (it will be created if not exists)
conn = sqlite3.connect(DB_NAME)

# Mapping of CSV filenames to table names
files_and_tables = {
    "Product-Level Ad Sales and Metrics (mapped).csv": "ad_sales",
    "Product-Level Total Sales and Metrics (mapped).csv": "total_sales",
    "Product-Level Eligibility Table (mapped).csv": "eligibility"
}

# Read each CSV and store it as a table in the SQLite database
for filename, table_name in files_and_tables.items():
    file_path = os.path.join(DATA_FOLDER, filename)
    try:
        df = pd.read_csv(file_path)
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"[✅] Table '{table_name}' created from '{filename}'")
    except Exception as e:
        print(f"[❌] Failed to load '{filename}': {e}")

# Close the connection
conn.close()
print("[✔️] All datasets have been loaded into the database successfully.")
