"""DVC stage 2 -- train: fit a scikit-learn Pipeline and persist it.

The preprocessing lives INSIDE the Pipeline on purpose: that is what removes the
training/serving skew class of bugs (week 5-6). Never ship separate scaler.pkl /
encoder.pkl files -- see the anti-pattern in context/MLSecOps/Gyakorlat/.

Run:  python -m src.churn.train      (or: dvc repro train)
"""

from __future__ import annotations
from typing import Any

import joblib
import pandas as pd
from pandas import DataFrame
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.churn import config

log = config.get_logger(__name__)


def build_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    """One-hot for object/category columns, scaling for numeric ones."""
    categorical = X.select_dtypes(include=["object", "category", "bool"]).columns.tolist()
    numeric = [c for c in X.columns if c not in categorical]
    log.info("categorical=%d numeric=%d", len(categorical), len(numeric))

    return ColumnTransformer(
        transformers=[
            (
                "cat",
                Pipeline(
                    [
                        ("impute", SimpleImputer(strategy="most_frequent")),
                        # handle_unknown='ignore': unseen categories at serving time
                        # must not crash the API (week 7).
                        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
                    ]
                ),
                categorical,
            ),
            (
                "num",
                Pipeline(
                    [
                        ("impute", SimpleImputer(strategy="median")),
                        ("scale", StandardScaler()),
                    ]
                ),
                numeric,
            ),
        ],
        remainder="drop",
    )


def build_estimator(model_name: str, seed: int, train_params: Any):
    if model_name == "random_forest":
        return RandomForestClassifier(
            n_estimators=train_params["n_estimators"],
            max_depth=train_params["max_depth"],
            min_samples_leaf=train_params["min_samples_leaf"],
            class_weight=train_params["class_weight"],
            random_state=seed,
            n_jobs=-1,
        )
    if model_name == "logistic_regression":
        return LogisticRegression(
            max_iter=1000,
            class_weight=train_params["class_weight"],
            random_state=seed,
        )
    raise ValueError(f"Unknown model: {model_name!r}")


def build_pipeline(
        X: pd.DataFrame, model_name: str, seed: int, train_params: Any) -> Pipeline:
    return Pipeline(
        [
            ("preprocess", build_preprocessor(X)),
            ("model", build_estimator(model_name, seed, train_params)),
        ]
    )


def main() -> None:
    params: dict[str, Any] = config.load_params()
    seed = params["seed"]
    target = params["prepare"]["target"]
    train_params = params["train"]

    train_df: DataFrame = pd.read_csv(config.TRAIN_CSV)
    X = train_df.drop(columns=[target])
    y = train_df[target]

    pipe: Pipeline = build_pipeline(X, train_params["model"], seed, train_params)
    log.info("Fitting %s on %d rows", train_params["model"], len(X))
    pipe.fit(X, y)

    config.ensure_dirs(config.MODELS_DIR)
    joblib.dump(pipe, config.MODEL_PATH)
    log.info("Model written to %s", config.MODEL_PATH)


if __name__ == "__main__":
    main()
