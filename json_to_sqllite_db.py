import json
import sqlite3

def create_table_from_json(cursor, table_name, data):
    """Create a table based on the JSON structure."""
    columns = []
    for key, value in data.items():
        # Define SQLite types based on Python types
        if isinstance(value, int):
            col_type = 'INTEGER'
        elif isinstance(value, float):
            col_type = 'REAL'
        elif isinstance(value, str):
            col_type = 'TEXT'
        elif isinstance(value, bool):
            col_type = 'INTEGER'  # SQLite stores booleans as INTEGER (1 or 0)
        elif isinstance(value, list):
            col_type = 'TEXT'  # Lists are stored as TEXT (we can later serialize them if needed)
        else:
            col_type = 'TEXT'  # Default type for unknown structures

        columns.append(f"{key} {col_type}")
    
    columns_definition = ", ".join(columns)
    create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_definition});"
    cursor.execute(create_table_sql)

def insert_data_into_table(cursor, table_name, data):
    """Insert data into the table."""
    columns = ', '.join(data.keys())
    placeholders = ', '.join('?' for _ in data)
    insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    cursor.execute(insert_sql, tuple(data.values()))

def create_index(cursor, table_name, column_name):
    """Create an index on a column to optimize queries."""
    create_index_sql = f"CREATE INDEX IF NOT EXISTS idx_{table_name}_{column_name} ON {table_name} ({column_name});"
    cursor.execute(create_index_sql)

def process_json_to_sqlite(json_file, sqlite_db):
    """Process the JSON file and generate the corresponding SQLite schema and data."""
    # Load JSON data
    with open(json_file, 'r') as f:
        json_data = json.load(f)
    
    # Connect to SQLite database
    conn = sqlite3.connect(sqlite_db)
    cursor = conn.cursor()

    # Iterate through the JSON data and create tables and insert data
    for table_name, data_list in json_data.items():
        if isinstance(data_list, list) and len(data_list) > 0:
            # Create table based on the first item in the list (assuming all items have the same structure)
            create_table_from_json(cursor, table_name, data_list[0])
            # Insert data into the table
            for data in data_list:
                insert_data_into_table(cursor, table_name, data)
                # Create index on frequently queried columns (optional step)
                for column in data.keys():
                    create_index(cursor, table_name, column)

    # Commit changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    json_file = "data.json"  # Replace with the path to your JSON file
    sqlite_db = "output.db"  # Replace with the desired SQLite database file
    process_json_to_sqlite(json_file, sqlite_db)
    print(f"SQLite database '{sqlite_db}' created from '{json_file}'")
