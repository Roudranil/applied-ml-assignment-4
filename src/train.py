import joblib
import numpy as np
import optuna
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import average_precision_score
from sklearn.model_selection import StratifiedKFold
from xgboost import XGBClassifier

DATA_PATH = "../data/raw-data.csv"


def prepare_dataset(data_path):
    data = pd.read_csv(data_path)
    X = data["text"]
    y = data["spam"]

    splitter = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    return X, y, splitter


def objective(trial: optuna.Trial):
    max_depth = trial.suggest_int("max_depth", 3, 7)
    learning_rate = trial.suggest_float("learning_rate", 0.001, 0.1)
    # min_child_weight = trial.suggest_float("min_child_weight", 1, 10)
    subsample = trial.suggest_float("subsample", 0.4, 0.7)
    colsample_bytree = trial.suggest_float("colsample_bytree", 0.4, 0.7)

    model = XGBClassifier(
        max_depth=max_depth,
        learning_rate=learning_rate,
        subsample=subsample,
        # min_child_weight=min_child_weight,
        colsample_bytree=colsample_bytree,
    )
    vectoriser = TfidfVectorizer()
    scores = []
    X, y, splitter = prepare_dataset(DATA_PATH)

    for i, (train_idx, val_idx) in enumerate(splitter.split(X, y)):
        X_train_cv = X.iloc[train_idx]
        X_val_cv = X.iloc[val_idx]

        y_train_cv = y.iloc[train_idx]
        y_val_cv = y.iloc[val_idx]

        X_train_cv = vectoriser.fit_transform(X_train_cv)
        X_val_cv = vectoriser.transform(X_val_cv)

        model.fit(X_train_cv, y_train_cv)
        y_pred = model.predict(X_val_cv)

        scores.append(-average_precision_score(y_val_cv, y_pred))

    return np.mean(scores)


def main():
    study = optuna.create_study()
    study.optimize(objective, n_trials=20)
    params = study.best_params
    X, y, _ = prepare_dataset(DATA_PATH)
    model = XGBClassifier(**params)
    vectoriser = TfidfVectorizer()
    X = vectoriser.fit_transform(X)
    model.fit(X, y)

    joblib.dump(vectoriser, "../model/vectoriser.pkl")
    joblib.dump(model, "../model/model.pkl")


if __name__ == "__main__":
    main()
