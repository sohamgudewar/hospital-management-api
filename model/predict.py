import os
import pickle
import pandas as pd

MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(MODEL_DIR, "model1.pkl")

# Load the trained machine learning pipeline
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

MODEL_VERSION = "1.0.0"

# Class labels for probability distribution
class_labels = model.classes_.tolist()


def predict_output(user_input: dict):
    df = pd.DataFrame([user_input])

    predicted_class = model.predict(df)[0]
    probabilities = model.predict_proba(df)[0]
    confidence = max(probabilities)

    class_probs = dict(zip(class_labels, [round(float(p), 4) for p in probabilities]))

    return {
        "predicted_category": str(predicted_class),
        "confidence": round(float(confidence), 4),
        "class_probabilities": class_probs
    }
