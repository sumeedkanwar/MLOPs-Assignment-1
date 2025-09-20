import os
import joblib
from app.api import app

# Path to the pre-trained model
MODEL_PATH = os.environ.get("MODEL_PATH", "artifacts/car_price_model.pkl")

# Load the model
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"Pre-trained model not found at '{MODEL_PATH}'. "
        "Please make sure the model exists before starting the app."
    )

model = joblib.load(MODEL_PATH)
print(f"Loaded pre-trained model from {MODEL_PATH}")

# Make the model accessible in your Flask routes if needed
# Example: attach it to the app object
app.model = model

# Start Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))