import sqlite3
import pandas as pd

def query_top_rated():
    db_path = 'data/soccer_research.db'
    conn = sqlite3.connect(db_path)
    
    print("\n--- 🏆 Top 5 Highest Rated Players in EA Sports FC 26 ---")
    
    # Simple SQL query to fetch specific performance indicators
    query = """
    SELECT firstname, lastname, position, overallrating 
    FROM players 
    ORDER BY overallrating DESC 
    LIMIT 5;
    """
    
    df = pd.read_sql_query(query, conn)
    print(df)
    
    conn.close()

if __name__ == "__main__":
    query_top_rated()
