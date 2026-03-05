import numpy as np
import joblib
import json
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier

BASE_DIR = Path(__file__).resolve().parent

NUM_FEATURES = 10
NUM_CLASSES = 6

# --------- Synthetic Training Data ---------
X = np.random.rand(5000, NUM_FEATURES)

y = []
for row in X:
    avg = np.mean(row)
    if avg > 0.85:
        y.append(5)  # DDoS
    elif avg > 0.70:
        y.append(1)  # DoS
    elif avg > 0.55:
        y.append(2)  # Probe
    elif avg > 0.40:
        y.append(3)  # R2L
    elif avg > 0.25:
        y.append(4)  # U2R
    else:
        y.append(0)  # Normal

y = np.array(y)

# --------- Train RandomForest ---------
model = RandomForestClassifier(n_estimators=150, random_state=42)
model.fit(X, y)

# --------- Save Model ---------
joblib.dump(model, BASE_DIR / "nids_model.pkl")

# Save feature names
features = [f"f{i}" for i in range(NUM_FEATURES)]
with open(BASE_DIR / "features.json", "w") as f:
    json.dump(features, f)

print("✅ Multi-class NIDS model trained successfully (scikit-learn)")