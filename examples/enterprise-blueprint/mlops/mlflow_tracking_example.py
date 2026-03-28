"""Minimal MLflow tracking example with a deterministic run name."""

from datetime import datetime, timezone

import mlflow
from sklearn.linear_model import LogisticRegression


def train_example_model(X_train, y_train):
    model = LogisticRegression(max_iter=200, random_state=42)
    model.fit(X_train, y_train)

    run_name = f"fraud_model_{datetime.now(timezone.utc).strftime('%Y%m%d')}"
    with mlflow.start_run(run_name=run_name):
        mlflow.log_param("algorithm", "logistic_regression")
        mlflow.log_param("max_iter", 200)
        mlflow.log_param("random_state", 42)
        mlflow.sklearn.log_model(model, "model")

    return model
