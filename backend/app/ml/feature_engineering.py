"""
Feature Engineering and Dataset Utilities (Stage 4)
Defines canonical psychological feature orders, class labels, and synthetic dataset generation.
"""
import os
from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np
import pandas as pd

# Canonical feature ordering for ML model training and inference
FEATURE_NAMES: List[str] = [
    "restlessness_score",
    "emotional_reactivity_score",
    "motivation_score",
    "energy_score",
    "concentration_score",
    "calmness_score",
    "routine_score",
    "overwhelm_score",
    "mental_clarity_score",
]

# Project-defined mental-wellness pattern labels (NOT medical diagnoses)
CLASS_LABELS: Dict[int, str] = {
    0: "Balanced / Stable",
    1: "Mild Mental Distress",
    2: "Moderate Mental Distress",
    3: "High Mental Distress",
}

LABEL_TO_CLASS: Dict[str, int] = {v: k for k, v in CLASS_LABELS.items()}


def extract_feature_vector(features: Union[Dict[str, float], Any]) -> np.ndarray:
    """
    Extracts a 1D numpy array of length 9 matching FEATURE_NAMES order.
    Accepts a dictionary or a Pydantic FeatureScores instance.
    """
    if hasattr(features, "model_dump"):
        feat_dict = features.model_dump()
    elif hasattr(features, "dict"):
        feat_dict = features.dict()
    elif isinstance(features, dict):
        feat_dict = features
    else:
        raise ValueError(f"Unsupported features object type: {type(features)}")

    vector = []
    for name in FEATURE_NAMES:
        if name not in feat_dict:
            raise KeyError(f"Missing required psychological feature: '{name}'")
        val = float(feat_dict[name])
        # Validate 1.0 - 5.0 range
        if not (1.0 <= val <= 5.0):
            # Clamp gently with a warning-level behavior to ensure robust inference
            val = max(1.0, min(5.0, val))
        vector.append(val)

    return np.array(vector, dtype=np.float32)


def generate_synthetic_development_dataset(
    samples_per_class: int = 300,
    random_state: int = 42,
    output_path: Optional[str] = None,
) -> pd.DataFrame:
    """
    Generates a reproducible, clearly labeled SYNTHETIC development dataset
    for establishing and testing the Scikit-learn Random Forest pipeline.

    IMPORTANT ACADEMIC DISCLAIMER:
    This dataset is synthetic and calibrated against standard psychological Likert
    distributions. It is used ONLY for demonstrating the AI/ML pipeline and MUST NOT
    be claimed as real clinical empirical data.
    """
    rng = np.random.RandomState(random_state)
    data_rows = []

    # Profiles define mean (mu) and standard deviation (sigma) for each feature
    # [restlessness, reactivity, motivation, energy, concentration, calmness, routine, overwhelm, clarity]
    class_profiles = {
        0: {  # Balanced / Stable: high calmness, clarity, routine; low restlessness, overwhelm
            "means": [1.4, 1.4, 4.3, 4.4, 4.3, 4.4, 4.3, 1.3, 4.4],
            "sigmas": [0.3, 0.3, 0.4, 0.4, 0.4, 0.3, 0.4, 0.3, 0.3],
        },
        1: {  # Mild Mental Distress: mild restlessness, occasional overwhelm, moderate calm
            "means": [2.6, 2.4, 3.4, 3.3, 3.3, 3.2, 3.2, 2.5, 3.3],
            "sigmas": [0.4, 0.4, 0.4, 0.5, 0.4, 0.4, 0.5, 0.4, 0.4],
        },
        2: {  # Moderate Mental Distress: higher restlessness, reactivity, overwhelm, lower calm
            "means": [3.7, 3.6, 2.4, 2.3, 2.4, 2.3, 2.3, 3.8, 2.4],
            "sigmas": [0.4, 0.4, 0.5, 0.5, 0.5, 0.4, 0.5, 0.4, 0.4],
        },
        3: {  # High Mental Distress: intense restlessness, severe overwhelm, low calm, sluggishness
            "means": [4.6, 4.5, 1.5, 1.4, 1.5, 1.3, 1.4, 4.7, 1.4],
            "sigmas": [0.3, 0.3, 0.4, 0.4, 0.4, 0.3, 0.4, 0.3, 0.3],
        },
    }

    for class_id, profile in class_profiles.items():
        means = profile["means"]
        sigmas = profile["sigmas"]

        for _ in range(samples_per_class):
            row = []
            for m, s in zip(means, sigmas):
                # Sample with normal distribution and clamp to Likert feature scale [1.0, 5.0]
                val = rng.normal(m, s)
                val = float(np.clip(np.round(val, 2), 1.0, 5.0))
                row.append(val)

            row.append(class_id)
            row.append(CLASS_LABELS[class_id])
            data_rows.append(row)

    columns = FEATURE_NAMES + ["wellness_class", "wellness_label"]
    df = pd.DataFrame(data_rows, columns=columns)

    # Shuffle dataset
    df = df.sample(frac=1.0, random_state=random_state).reset_index(drop=True)

    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        # Write dataset with explicit synthetic header comment
        header_comment = (
            "# SYNTHETIC DEVELOPMENT DATASET ONLY\n"
            "# Created for AI Mental Wellness System (Academic IKS Project)\n"
            "# Do NOT use as empirical clinical evidence.\n"
        )
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(header_comment)
            df.to_csv(f, index=False)

    return df
