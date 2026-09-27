"""
Model Inference Module (Stage 4)
Loads trained Random Forest classifier and generates mental wellness pattern predictions.
"""
from typing import Dict, Any, Union, Optional
import numpy as np
from app.ml.feature_engineering import (
    FEATURE_NAMES,
    CLASS_LABELS,
    extract_feature_vector,
)
from app.ml.model_utils import load_model_artifacts, is_model_trained

# In-memory model cache to avoid re-reading disk on every API call
_MODEL_CACHE = None
_METADATA_CACHE = None


def get_or_load_model() -> tuple:
    """
    Retrieves the cached model or loads it from disk.
    If not yet trained on disk, triggers initial model training.
    """
    global _MODEL_CACHE, _METADATA_CACHE

    if _MODEL_CACHE is not None:
        return _MODEL_CACHE, _METADATA_CACHE

    if not is_model_trained():
        # Auto-train initial model if running for the first time
        from app.ml.train_model import train_and_evaluate_model
        _MODEL_CACHE, _METADATA_CACHE = train_and_evaluate_model()
        return _MODEL_CACHE, _METADATA_CACHE

    _MODEL_CACHE, _METADATA_CACHE = load_model_artifacts()
    return _MODEL_CACHE, _METADATA_CACHE


def predict_wellness_state(features: Union[Dict[str, float], Any]) -> Dict[str, Any]:
    """
    Classifies the user's psychological feature vector into a wellness state.
    
    Returns:
    {
        "predicted_class": int (0 to 3),
        "predicted_label": str ("Balanced / Stable", etc.),
        "confidence": float (0.0 to 1.0),
        "class_probabilities": Dict[str, float],
        "feature_values": Dict[str, float],
        "top_features": Dict[str, float]
    }
    """
    # 1. Feature extraction and validation
    feature_vector = extract_feature_vector(features)  # Shape (9,)
    X_input = feature_vector.reshape(1, -1)

    # 2. Model retrieval
    model, metadata = get_or_load_model()

    # 3. Model inference
    pred_class_idx = int(model.predict(X_input)[0])
    probabilities = model.predict_proba(X_input)[0]  # Array of length 4

    confidence = round(float(probabilities[pred_class_idx]), 4)
    predicted_label = CLASS_LABELS.get(pred_class_idx, "Unknown State")

    # Format class probabilities map
    class_probabilities = {
        CLASS_LABELS[i]: round(float(prob), 4) for i, prob in enumerate(probabilities)
    }

    # Format feature values map
    feature_values = {
        name: round(float(val), 2) for name, val in zip(FEATURE_NAMES, feature_vector)
    }

    return {
        "predicted_class": pred_class_idx,
        "predicted_label": predicted_label,
        "confidence": confidence,
        "class_probabilities": class_probabilities,
        "feature_values": feature_values,
        "model_type": "RandomForestClassifier",
        "disclaimer": (
            "Academic ML pattern classification based on self-reported Likert features. "
            "This is NOT a psychiatric diagnosis or clinical evaluation."
        ),
    }
