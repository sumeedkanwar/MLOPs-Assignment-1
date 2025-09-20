
import os
from app.api import app

MODEL_PATH = os.environ.get("MODEL_PATH", "artifacts/car_price_model.pkl")

# If you prefer to always retrain comment out the if-check below
if not os.path.exists(MODEL_PATH):
    # If you want to train here, call your training routine. If model.py is standalone, use subprocess or import.
    # For simplicity, we attempt to import and run model.py's train routine if present.
    try:
        # This expects app/model.py to expose a function train_and_save_model(...)
        from app.model import train_and_save_model
        print("Training model because artifact missing...")
        train_and_save_model("data/raw/pakwheels.csv", MODEL_PATH)
    except Exception as e:
        print("Could not auto-train model. Please run `python app/model.py` manually. Error:", e)

# Start Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
