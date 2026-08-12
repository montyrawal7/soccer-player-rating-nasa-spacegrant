import sqlite3
import pandas as pd

def inspect_database():
    db_path = 'data/soccer_research.db'
    conn = sqlite3.connect(db_path)
    
    print("\n--- 🔍 1. Database Table Architecture Info ---")
    # Query the database to list out column names and structural data types
    table_info = pd.read_sql_query("PRAGMA table_info(players);", conn)
    print(f"Total Columns Registered: {len(table_info)}")
    print(table_info[['name', 'type']].head(15)) # Prints the first 15 columns
    
    print("\n--- 📋 2. Full Content View ---")
    # Pull all contents currently loaded into the table
    all_players = pd.read_sql_query("SELECT * FROM players;", conn)
    print(f"Total Rows Found: {len(all_players)}")
    print(all_players.head(10))
    
    conn.close()

if __name__ == "__main__":
    inspect_database()
