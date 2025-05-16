import json
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification

with open('config.json') as f:
    config = json.load(f)

def load_or_train_model():
    try:
        return joblib.load(config["model_path"])
    except FileNotFoundError:
        X, y = make_classification(n_samples=100, n_features=5, n_classes=2)
        model = LogisticRegression()
        model.fit(X, y)
        joblib.dump(model, config["model_path"])
        return model

def predict(features):
    model = load_or_train_model()
    return model.predict(features)