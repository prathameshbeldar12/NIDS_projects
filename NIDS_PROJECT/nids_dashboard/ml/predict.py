import numpy as np
import joblib
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Load model
model = joblib.load(BASE_DIR / "nids_model.pkl")

# Class labels
CLASS_LABELS = {
    0: "Normal",
    1: "DoS",
    2: "Probe",
    3: "R2L",
    4: "U2R",
    5: "DDoS",
}

def detect_attack(feature_row):
    try:
        # Convert string values to float
        features = np.array(feature_row, dtype=float).reshape(1, -1)

        # Predict class
        prediction = model.predict(features)[0]

        attack_type = CLASS_LABELS[int(prediction)]

        # Confidence
        probs = model.predict_proba(features)[0]
        confidence = round(float(max(probs)) * 100, 2)

        # Set severity
        if attack_type == "Normal":
            severity = "Low"
        elif attack_type in ["Probe"]:
            severity = "Medium"
        elif attack_type in ["DoS", "R2L", "U2R"]:
            severity = "High"
        else:
            severity = "Critical"

        return {
            "attack": attack_type,
            "severity": severity,
            "confidence": confidence
        }

    except Exception as e:
        print("Prediction Error:", e)
        return {
            "attack": "Normal",
            "severity": "Low",
            "confidence": 0.0
        }