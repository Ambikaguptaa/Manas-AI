"""
Machine Learning Module for Mental Wellness Assessment (Stage 4)
Provides Scikit-learn Random Forest classification, evaluation, and feature extraction.
"""
from app.ml.feature_engineering import (
    FEATURE_NAMES,
    CLASS_LABELS,
    LABEL_TO_CLASS,
    extract_feature_vector,
    generate_synthetic_development_dataset,
)
from app.ml.train_model import train_and_evaluate_model
from app.ml.predict import predict_wellness_state
from app.ml.model_utils import is_model_trained, load_model_artifacts

__all__ = [
    "FEATURE_NAMES",
    "CLASS_LABELS",
    "LABEL_TO_CLASS",
    "extract_feature_vector",
    "generate_synthetic_development_dataset",
    "train_and_evaluate_model",
    "predict_wellness_state",
    "is_model_trained",
    "load_model_artifacts",
]
