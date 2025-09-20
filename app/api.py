from flask import Flask, request, jsonify
import pickle
import os
import numpy as np
import pandas as pd
from app.preprocess import basic_clean, select_features

app = Flask(__name__)

MODEL_PATH = os.environ.get("MODEL_PATH", "artifacts/car_price_model.pkl")

# Load pipeline (preprocessor + model) at startup
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Run training first.")

with open(MODEL_PATH, "rb") as f:
    pipeline = pickle.load(f)

@app.route("/")
def index():
    return jsonify({"message": "PakWheels price predictor - send POST to /predict"}), 200

@app.route("/predict", methods=["POST"])
def predict_price():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON body"}), 400

    # Accept either single object or { "rows": [ ... ] }
    if isinstance(data, dict) and "rows" in data:
        rows = data["rows"]
    elif isinstance(data, list):
        rows = data
    else:
        rows = [data]

    df = pd.DataFrame(rows)
    df = basic_clean(df)

    # Validate needed columns
    required = ['age', 'mileage', 'fuel_type', 'transmission', 'city', 'registered', 'assembly']
    missing = [c for c in required if c not in df.columns]
    if missing:
        return jsonify({"error": f"Missing required fields: {missing}"}), 400

    X, _ = select_features(df)

    try:
        preds_log = pipeline.predict(X)  # predictions are log1p(price)
    except Exception as e:
        return jsonify({"error": f"Model prediction error: {str(e)}"}), 500

    # invert log1p -> price in PKR
    preds = np.expm1(preds_log)
    preds = [float(max(0.0, p)) for p in preds]  # no negative prices

    # Return single object or list based on input
    if len(preds) == 1:
        return jsonify({"predicted_price": preds[0]}), 200
    else:
        return jsonify({"predicted_prices": preds}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
