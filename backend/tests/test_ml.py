"""
Automated Unit and Integration Tests for the Machine Learning Module (Stage 4)
"""
import pytest
import numpy as np
from app.ml.feature_engineering import (
    FEATURE_NAMES,
    CLASS_LABELS,
    extract_feature_vector,
    generate_synthetic_development_dataset,
)
from app.ml.model_utils import is_model_trained, load_model_artifacts
from app.ml.predict import predict_wellness_state
from app.schemas.assessment import FeatureScores


def test_feature_vector_extraction():
    """
    Test extraction of 9 canonical features from a dictionary and FeatureScores object.
    """
    raw_dict = {
        "restlessness_score": 1.5,
        "emotional_reactivity_score": 2.0,
        "motivation_score": 4.5,
        "energy_score": 4.0,
        "concentration_score": 4.2,
        "calmness_score": 4.5,
        "routine_score": 4.0,
        "overwhelm_score": 1.2,
        "mental_clarity_score": 4.3,
    }

    vec = extract_feature_vector(raw_dict)
    assert isinstance(vec, np.ndarray)
    assert vec.shape == (9,)
    assert vec[0] == 1.5  # restlessness_score
    assert vec[7] == 1.2  # overwhelm_score

    # Test with Pydantic model
    fs = FeatureScores(**raw_dict)
    vec_pydantic = extract_feature_vector(fs)
    assert np.allclose(vec, vec_pydantic)


def test_synthetic_dataset_generation():
    """
    Test generation of reproducible synthetic development dataset.
    """
    df = generate_synthetic_development_dataset(samples_per_class=20, random_state=42)
    assert len(df) == 80  # 4 classes * 20
    for col in FEATURE_NAMES:
        assert col in df.columns
    assert "wellness_class" in df.columns
    assert "wellness_label" in df.columns

    # Verify class distribution
    counts = df["wellness_class"].value_counts().to_dict()
    assert counts == {0: 20, 1: 20, 2: 20, 3: 20}


def test_model_artifacts_exist_and_load():
    """
    Verify that trained model binary and metadata exist and load correctly.
    """
    assert is_model_trained() is True

    model, metadata = load_model_artifacts()
    assert hasattr(model, "predict")
    assert hasattr(model, "predict_proba")
    assert "metrics" in metadata
    assert "accuracy" in metadata["metrics"]
    assert "confusion_matrix" in metadata["metrics"]
    assert "feature_importances" in metadata
    assert "disclaimer" in metadata


def test_predict_wellness_state_balanced():
    """
    Test prediction on a calm, high-wellness feature profile.
    Should classify into Class 0 (Balanced / Stable).
    """
    balanced_features = {
        "restlessness_score": 1.2,
        "emotional_reactivity_score": 1.2,
        "motivation_score": 4.5,
        "energy_score": 4.5,
        "concentration_score": 4.5,
        "calmness_score": 4.8,
        "routine_score": 4.5,
        "overwhelm_score": 1.1,
        "mental_clarity_score": 4.6,
    }

    pred = predict_wellness_state(balanced_features)

    # Required output fields per user specification:
    assert "predicted_class" in pred
    assert "predicted_label" in pred
    assert "confidence" in pred
    assert "feature_values" in pred
    assert "class_probabilities" in pred

    assert pred["predicted_class"] == 0
    assert pred["predicted_label"] == "Balanced / Stable"
    assert 0.0 <= pred["confidence"] <= 1.0
    assert sum(pred["class_probabilities"].values()) == pytest.approx(1.0, abs=0.01)


def test_predict_wellness_state_high_distress():
    """
    Test prediction on an agitated, highly overwhelmed feature profile.
    Should classify into Class 3 (High Mental Distress).
    """
    distressed_features = {
        "restlessness_score": 4.8,
        "emotional_reactivity_score": 4.6,
        "motivation_score": 1.4,
        "energy_score": 1.2,
        "concentration_score": 1.5,
        "calmness_score": 1.2,
        "routine_score": 1.3,
        "overwhelm_score": 4.9,
        "mental_clarity_score": 1.3,
    }

    pred = predict_wellness_state(distressed_features)

    assert pred["predicted_class"] == 3
    assert pred["predicted_label"] == "High Mental Distress"
    assert pred["confidence"] >= 0.70
