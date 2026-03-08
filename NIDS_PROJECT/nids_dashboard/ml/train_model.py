import numpy as np
import joblib
import json
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier

BASE_DIR = Path(__file__).resolve().parent

NUM_FEATURES = 10

# -----------------------------------
# Generate Synthetic Dataset
# -----------------------------------

np.random.seed(42)

# Normal Traffic
normal = np.random.uniform(0.0, 0.25, (1000, NUM_FEATURES))

# R2L Attack
r2l = np.random.uniform(0.25, 0.40, (800, NUM_FEATURES))

# Probe Attack
probe = np.random.uniform(0.40, 0.55, (800, NUM_FEATURES))

# DoS Attack
dos = np.random.uniform(0.55, 0.75, (800, NUM_FEATURES))

# U2R Attack
u2r = np.random.uniform(0.75, 0.90, (800, NUM_FEATURES))

# DDoS Attack
ddos = np.random.uniform(0.90, 1.00, (800, NUM_FEATURES))


# Combine Features
X = np.vstack((normal, r2l, probe, dos, u2r, ddos))


# Labels
y = np.array(
    [0]*1000 +   # Normal
    [3]*800 +    # R2L
    [2]*800 +    # Probe
    [1]*800 +    # DoS
    [4]*800 +    # U2R
    [5]*800      # DDoS
)

# -----------------------------------
# Train RandomForest Model
# -----------------------------------

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X, y)


# -----------------------------------
# Save Model
# -----------------------------------

joblib.dump(model, BASE_DIR / "nids_model.pkl")


# Save Feature Names
features = [f"f{i}" for i in range(NUM_FEATURES)]

with open(BASE_DIR / "features.json", "w") as f:
    json.dump(features, f)


# Label Mapping
labels = {
    0: "Normal",
    1: "DoS",
    2: "Probe",
    3: "R2L",
    4: "U2R",
    5: "DDoS"
}

with open(BASE_DIR / "labels.json", "w") as f:
    json.dump(labels, f)


print("✅ NIDS Model Trained Successfully")
print("📁 Files Generated:")
print(" - nids_model.pkl")
print(" - features.json")
print(" - labels.json")