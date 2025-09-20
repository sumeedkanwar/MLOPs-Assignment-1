import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from scipy.stats import randint

# Load dataset
df = pd.read_csv("data/raw/pakwheels.csv")
df = df.dropna(subset=["price"])

# Feature engineering
df["age"] = 2025 - df["model"]
df = df[(df["price"] > 0) & (df["price"] < 40_000_000)]  # remove extreme outliers
df["price"] = np.log1p(df["price"])

X = df[["age", "mileage", "fuel_type", "transmission", "city", "registered", "assembly"]]
y = df["price"]

categorical = ["fuel_type", "transmission", "city", "registered", "assembly"]
numeric = ["age", "mileage"]

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
        ("num", "passthrough", numeric)
    ]
)

# Base model
rf = RandomForestRegressor(random_state=42, n_jobs=-1)

# Randomized search for hyperparameters
param_dist = {
    "model__n_estimators": randint(200, 800),
    "model__max_depth": randint(5, 30),
    "model__min_samples_split": randint(2, 10),
    "model__min_samples_leaf": randint(1, 5),
    "model__max_features": ["sqrt", "log2", None]  # removed "auto"
}

pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model", rf)
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

search = RandomizedSearchCV(
    pipeline,
    param_distributions=param_dist,
    n_iter=20,
    scoring="r2",
    cv=3,
    verbose=1,
    random_state=42,
    n_jobs=-1
)

search.fit(X_train, y_train)

best_model = search.best_estimator_
y_pred = best_model.predict(X_test)

r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print("Best parameters:", search.best_params_)
print(f"Model R^2 on test set: {r2:.4f}")
print(f"Model RMSE on test set: {rmse:.4f} (log scale)")

with open("artifacts/car_price_model.pkl", "wb") as f:
    pickle.dump(best_model, f)

print("✅ Tuned model saved to artifacts/car_price_model.pkl")
