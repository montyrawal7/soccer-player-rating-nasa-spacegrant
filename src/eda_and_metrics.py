import os
import sqlite3
import pandas as pd
from sklearn.preprocessing import StandardScaler

DB_PATH = os.path.join("data", "soccer_research.db")

def run_eda_and_feature_engineering():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database not found at {DB_PATH}. Run database_init.py first.")

    # 1. Connect to SQLite and load data
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM players;", conn)
    conn.close()

    print("=== EXPLORATORY DATA ANALYSIS (EDA) ===")
    print(f"Total Database Records: {len(df)}")
    
    # Identify numeric attribute columns for scaling
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    # Filter out ID or Rank columns from feature scaling
    feature_cols = [c for c in numeric_cols if c not in ['id', 'rank']]

    print(f"\nExtracted {len(feature_cols)} numeric attributes for feature engineering.")
    
    # 2. Compute Baseline Statistical Distributions (Mean & Std Dev)
    stats_summary = df[feature_cols].describe().T[['mean', 'std', 'min', '50%', 'max']]
    print("\nSample Baseline Distributions (First 5 Attributes):")
    print(stats_summary.head(5))

    # 3. Feature Engineering: Fit StandardScaler Engine
    scaler = StandardScaler()
    scaled_array = scaler.fit_transform(df[feature_cols])
    
    scaled_df = pd.DataFrame(scaled_array, columns=[f"{col}_zscore" for col in feature_cols])
    
    print("\n=== FEATURE ENGINEERING COMPLETE ===")
    print(f"Engineered {scaled_df.shape[1]} normalized Z-score feature columns.")
    print("Sample Normalized Output (First 3 Rows):")
    print(scaled_df.head(3))

if __name__ == "__main__":
    run_eda_and_feature_engineering()

