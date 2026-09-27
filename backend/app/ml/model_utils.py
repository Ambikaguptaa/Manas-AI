"""
Model Persistence and Utility Functions (Stage 4)
Handles saving, loading, and metadata inspection for the Scikit-learn Random Forest model.
"""
import os
import json
from typing import Dict, Any, Tuple, Optional
import joblib

# Determine artifact paths relative to this file
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ARTIFACTS_DIR = os.path.join(CURRENT_DIR, "artifacts")
MODEL_PATH = os.path.join(ARTIFACTS_DIR, "random_forest_wellness_model.joblib")
METADATA_PATH = os.path.join(ARTIFACTS_DIR, "model_metadata.json")


def save_model_artifacts(
    model: Any,
    metrics: Dict[str, Any],
    feature_importances: Dict[str, float],
    training_info: Optional[Dict[str, Any]] = None,
) -> Tuple[str, str]:
    """
    Saves the trained Random Forest model and its evaluation metadata.
    """
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)

    # 1. Save model binary
    joblib.dump(model, MODEL_PATH)

    # 2. Save metadata JSON
    metadata = {
        "model_type": "RandomForestClassifier",
        "library": "scikit-learn",
        "dataset_type": "Synthetic Development Dataset (Educational / Academic Project)",
        "disclaimer": (
            "This model is calibrated on synthetic Likert feature distributions for academic demonstration. "
            "It does NOT represent clinical medical diagnosis."
        ),
        "metrics": metrics,
        "feature_importances": feature_importances,
        "training_info": training_info or {},
    }

    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    return MODEL_PATH, METADATA_PATH


def load_model_artifacts() -> Tuple[Any, Dict[str, Any]]:
    """
    Loads the serialized Random Forest model and associated metadata.
    Raises FileNotFoundError if artifacts have not been trained yet.
    """
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Trained model artifact not found at {MODEL_PATH}. "
            "Please run 'train_model.py' to train the initial Random Forest classifier."
        )

    model = joblib.load(MODEL_PATH)
    metadata = {}
    if os.path.exists(METADATA_PATH):
        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            metadata = json.load(f)

    return model, metadata


def is_model_trained() -> bool:
    """
    Checks whether the model binary already exists on disk.
    """
    return os.path.exists(MODEL_PATH)
