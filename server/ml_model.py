import numpy as np
from sklearn.ensemble import IsolationForest

model = IsolationForest(contamination=0.1)

# Dummy training
X = np.array([
    [10, 1, 2],
    [20, 2, 3],
    [5, 1, 1]
])

model.fit(X)


def predict_anomaly(features):
    vector = [[
        features["session_duration"],
        features["join_frequency"],
        features["recent_activity"]
    ]]

    pred = model.predict(vector)

    return "ANOMALY" if pred[0] == -1 else "NORMAL"