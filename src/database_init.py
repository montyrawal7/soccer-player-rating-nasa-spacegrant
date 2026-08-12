import os
import sqlite3
import pandas as pd

CSV_PATH = os.path.join("data", "ea_fc26_players.csv")
DB_PATH = os.path.join("data", "soccer_research.db")

def clean_and_ingest():
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"Missing {CSV_PATH}. Please run download_data.py first.")

    print("Reading raw dataset...")
    df = pd.read_csv(CSV_PATH)
    
    # Standardize column headers to lowercase to avoid case-sensitivity KeyErrors
    df.columns = df.columns.str.strip().str.lower()
    
    print(f"Detected CSV Columns: {list(df.columns[:10])}...")

    # Identify existing columns flexible to common CSV variations
    name_col = next((c for c in ['name', 'short_name', 'long_name', 'player_name'] if c in df.columns), None)
    age_col = next((c for c in ['age'] if c in df.columns), None)
    pace_col = next((c for c in ['pace', 'pace_total', 'sprint_speed'] if c in df.columns), None)
    dribbling_col = next((c for c in ['dribbling', 'dribbling_total'] if c in df.columns), None)

    # 1. Drop rows missing critical columns if found
    check_cols = [c for c in [name_col, age_col, pace_col, dribbling_col] if c is not None]
    
    initial_count = len(df)
    if check_cols:
        df.dropna(subset=check_cols, inplace=True)
    
    # 2. Filter out non-positive values for numeric stats
    numeric_cols = [c for c in ['pace', 'acceleration', 'sprint_speed', 'strength', 'stamina', 'agility', 'dribbling'] if c in df.columns]
    for col in numeric_cols:
        df = df[df[col] > 0]

    cleaned_count = len(df)
    print(f"Data Cleaning Complete: Retained {cleaned_count} / {initial_count} valid player records.")

    # 3. Ingest into SQLite Database
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    
    print(f"Writing cleaned data to SQLite database at {DB_PATH}...")
    df.to_sql("players", conn, if_exists="replace", index=False)
    
    # Verify table row count
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM players;")
    row_count = cursor.fetchone()[0]
    conn.close()

    print(f"Success! SQLite table 'players' created with {row_count} records.")

if __name__ == "__main__":
    clean_and_ingest()


