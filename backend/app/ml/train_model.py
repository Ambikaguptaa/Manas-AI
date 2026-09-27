"""
Model Training Pipeline (Stage 4)
Trains and evaluates a Scikit-learn Random Forest Classifier for mental wellness pattern recognition.
Computes accuracy, precision, recall, F1-score, and confusion matrix.
"""
import os
import sys
from datetime import datetime
from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)

# Ensure app package is importable when script is executed directly
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.ml.feature_engineering import (
    FEATURE_NAMES,
    CLASS_LABELS,
    generate_synthetic_development_dataset,
)
from app.ml.model_utils import save_model_artifacts


def train_and_evaluate_model(
    samples_per_class: int = 300,
    test_size: float = 0.2,
    random_state: int = 42,
    n_estimators: int = 100,
    max_depth: int = 6,
    dataset_csv_path: str = None,
) -> Tuple[RandomForestClassifier, Dict[str, Any]]:
    """
    Executes the end-to-end model training and validation workflow:
    1. Loads or generates synthetic development dataset.
    2. Performs stratified train/test split.
    3. Trains RandomForestClassifier.
    4. Evaluates comprehensive multi-class metrics (Accuracy, Precision, Recall, F1, Confusion Matrix).
    5. Saves model binary and evaluation metadata to disk.
    """
    if dataset_csv_path is None:
        dataset_csv_path = os.path.join(backend_dir, "..", "data", "synthetic_wellness_dataset.csv")

    # Generate or load dataset
    print(f"Generating synthetic development dataset ({samples_per_class * 4} samples)...")
    df = generate_synthetic_development_dataset(
        samples_per_class=samples_per_class,
        random_state=random_state,
        output_path=dataset_csv_path,
    )

    X = df[FEATURE_NAMES].values
    y = df["wellness_class"].values.astype(int)

    # 80/20 Stratified train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )

    # Initialize Random Forest Classifier
    rf_model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_split=4,
        random_state=random_state,
    )

    # Fit model on training partition
    rf_model.fit(X_train, y_train)

    # Predict on unseen test partition
    y_pred = rf_model.predict(X_test)

    # Calculate multi-class evaluation metrics
    acc = float(accuracy_score(y_test, y_pred))
    prec_weighted = float(precision_score(y_test, y_pred, average="weighted", zero_division=0))
    rec_weighted = float(recall_score(y_test, y_pred, average="weighted", zero_division=0))
    f1_weighted = float(f1_score(y_test, y_pred, average="weighted", zero_division=0))

    prec_macro = float(precision_score(y_test, y_pred, average="macro", zero_division=0))
    rec_macro = float(recall_score(y_test, y_pred, average="macro", zero_division=0))
    f1_macro = float(f1_score(y_test, y_pred, average="macro", zero_division=0))

    cm = confusion_matrix(y_test, y_pred).tolist()
    class_report = classification_report(
        y_test,
        y_pred,
        target_names=[CLASS_LABELS[i] for i in range(4)],
        output_dict=True,
        zero_division=0,
    )

    # Extract feature importances
    importances = rf_model.feature_importances_
    sorted_idx = np.argsort(importances)[::-1]
    feature_importances = {
        FEATURE_NAMES[idx]: round(float(importances[idx]), 4) for idx in sorted_idx
    }

    metrics = {
        "accuracy": round(acc, 4),
        "precision_weighted": round(prec_weighted, 4),
        "recall_weighted": round(rec_weighted, 4),
        "f1_score_weighted": round(f1_weighted, 4),
        "precision_macro": round(prec_macro, 4),
        "recall_macro": round(rec_macro, 4),
        "f1_score_macro": round(f1_macro, 4),
        "confusion_matrix": cm,
        "classification_report": class_report,
        "test_sample_count": len(y_test),
        "train_sample_count": len(y_train),
    }

    training_info = {
        "timestamp": datetime.now().isoformat(),
        "random_state": random_state,
        "n_estimators": n_estimators,
        "max_depth": max_depth,
        "test_size": test_size,
        "classes": CLASS_LABELS,
    }

    # Save artifacts to backend/app/ml/artifacts/
    model_file, meta_file = save_model_artifacts(
        model=rf_model,
        metrics=metrics,
        feature_importances=feature_importances,
        training_info=training_info,
    )

    print("\n=======================================================")
    print("  Random Forest Model Training Completed Successfully")
    print("=======================================================")
    print(f"Dataset Size: {len(df)} samples ({len(X_train)} train, {len(X_test)} test)")
    print(f"Accuracy:           {metrics['accuracy'] * 100:.2f}%")
    print(f"F1-Score (Weighted): {metrics['f1_score_weighted'] * 100:.2f}%")
    print(f"Precision:          {metrics['precision_weighted'] * 100:.2f}%")
    print(f"Recall:             {metrics['recall_weighted'] * 100:.2f}%")
    print("\nConfusion Matrix:")
    for row in metrics["confusion_matrix"]:
        print(" ", row)
    print("\nTop 3 Contributing Features:")
    for i, (feat, score) in enumerate(list(feature_importances.items())[:3]):
        print(f"  {i+1}. {feat}: {score:.4f}")
    print(f"\nModel saved to: {model_file}")
    print(f"Metadata saved to: {meta_file}")
    print("=======================================================\n")

    return rf_model, metrics


if __name__ == "__main__":
    train_and_evaluate_model()
