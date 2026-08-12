import os
import sqlite3
import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error

DB_PATH = os.path.join("data", "soccer_research.db")
MODEL_DIR = "models"

def train_and_evaluate_models():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database missing at {DB_PATH}. Run database_init.py first.")

    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM players;", conn)
    conn.close()

    target_col = 'overallrating'
    ignore_cols = ['id', 'rank', 'firstname', 'lastname', 'commonname', 'birthdate', target_col]
    feature_cols = [col for col in df.select_dtypes(include=['int64', 'float64']).columns if col not in ignore_cols]

    X = df[feature_cols]
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("=== MODEL TRAINING & EVALUATION ===")

    # Train production XGBoost model
    xgb_model = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
    xgb_model.fit(X_train, y_train)
    predictions = xgb_model.predict(X_test)

    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    mae = mean_absolute_error(y_test, predictions)

    print(f"[XGBoost Regressor] Saved to production -> RMSE: {rmse:.4f} | MAE: {mae:.4f}")

    # Save model and metadata for Streamlit app
    os.makedirs(MODEL_DIR, exist_ok=True)
    xgb_model.save_model(os.path.join(MODEL_DIR, "xgboost_model.json"))

    with open(os.path.join(MODEL_DIR, "feature_columns.json"), "w") as f:
        json.dump(feature_cols, f)

    print(f"Model artifacts saved successfully in '{MODEL_DIR}/'.")

if __name__ == "__main__":
    train_and_evaluate_models()

