import pandas as pd
import numpy as np

def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def basic_clean(df: pd.DataFrame) -> pd.DataFrame:
    """Minimal cleaning used both at training and for single-row API inputs."""
    # Keep only rows with price and numeric model/mileage where applicable
    if 'price' in df.columns:
        df = df.dropna(subset=['price'])
        df = df[df['price'] > 0]

    # Ensure numeric types
    if 'model' in df.columns:
        df = df.dropna(subset=['model'])
        df['model'] = pd.to_numeric(df['model'], errors='coerce')

    if 'mileage' in df.columns:
        df = df.dropna(subset=['mileage'])
        df['mileage'] = pd.to_numeric(df['mileage'], errors='coerce')

    # Fill categorical NaNs with 'Unknown'
    cat_cols = ['fuel_type', 'transmission', 'city', 'registered', 'assembly', 'color']
    for c in cat_cols:
        if c in df.columns:
            df[c] = df[c].fillna('Unknown')

    # Age column (consistent with training)
    if 'model' in df.columns:
        df['age'] = 2025 - df['model']

    return df

def select_features(df: pd.DataFrame):
    """Return X (features) and y if price exists. Feature set must match training X columns."""
    features = ['age', 'mileage', 'fuel_type', 'transmission', 'city', 'registered', 'assembly']
    X = df[features].copy()
    y = df['price'] if 'price' in df.columns else None
    return X, y
