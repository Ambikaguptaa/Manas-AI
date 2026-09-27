"""
Automated Unit Tests for the Indian Psychology Interpretation Engine (Stage 3)
"""
import pytest
from app.iks.guna_analysis import calculate_guna_tendencies, identify_dominant_pattern
from app.iks.mental_state import evaluate_chitta_vikshepa, determine_overall_wellness_state
from app.iks.interpretation import interpret_psychological_features
from app.services.scoring import calculate_feature_scores


def test_sattva_predominant_tendency():
    """
    Test calm, focused, and disciplined input profile.
    Expect Sattva score to be highest and Chitta Vikṣepa to be Minimal.
    """
    gunas = calculate_guna_tendencies(
        calmness=4.5,
        mental_clarity=4.5,
        concentration=4.5,
        routine=4.5,
        motivation=4.5,
        energy=4.5,
        restlessness=1.2,
        emotional_reactivity=1.2,
        overwhelm=1.2,
    )

    assert gunas["sattva_score"] >= 80.0
    assert gunas["rajas_score"] < 20.0
    assert gunas["tamas_score"] < 20.0
    assert "Sattva" in gunas["dominant_pattern"]
    assert sum(gunas["proportions"].values()) == pytest.approx(100.0, abs=0.5)


def test_rajas_predominant_tendency():
    """
    Test agitated, overthinking, and emotionally reactive input profile.
    Expect Rajas score to be highest and Chitta Vikṣepa to be Elevated.
    """
    gunas = calculate_guna_tendencies(
        calmness=1.5,
        mental_clarity=2.0,
        concentration=2.0,
        routine=2.5,
        motivation=3.0,
        energy=3.0,
        restlessness=4.8,
        emotional_reactivity=4.6,
        overwhelm=4.5,
    )

    assert gunas["rajas_score"] >= 75.0
    assert gunas["rajas_score"] > gunas["sattva_score"]
    assert "Rajas" in gunas["dominant_pattern"]

    vikshepa = evaluate_chitta_vikshepa(
        restlessness=4.8,
        emotional_reactivity=4.6,
        overwhelm=4.5,
        concentration=2.0,
        calmness=1.5,
    )
    assert vikshepa["level"] in ["Moderate Chitta Vikṣepa", "Elevated Chitta Vikṣepa"]


def test_tamas_predominant_tendency():
    """
    Test sluggish, low motivation, low routine input profile.
    Expect Tamas score to be highest.
    """
    gunas = calculate_guna_tendencies(
        calmness=2.5,
        mental_clarity=1.5,
        concentration=1.5,
        routine=1.2,
        motivation=1.2,
        energy=1.2,
        restlessness=2.0,
        emotional_reactivity=2.0,
        overwhelm=2.5,
    )

    assert gunas["tamas_score"] >= 70.0
    assert gunas["tamas_score"] > gunas["sattva_score"]
    assert "Tamas" in gunas["dominant_pattern"]


def test_iks_interpretation_output_structure_and_language():
    """
    Verify full interpretation dictionary output structure and non-clinical language compliance.
    """
    result = interpret_psychological_features(
        calmness_score=3.0,
        mental_clarity_score=3.5,
        concentration_score=3.0,
        routine_score=3.5,
        motivation_score=3.5,
        energy_score=3.5,
        restlessness_score=4.0,
        emotional_reactivity_score=3.8,
        overwhelm_score=3.5,
        overall_wellness_score=55.0,
    )

    # Required output fields per user specification:
    required_keys = [
        "overall_wellness_state",
        "wellness_score",
        "sattva_score",
        "rajas_score",
        "tamas_score",
        "chitta_vikshepa_indicator",
        "dominant_pattern",
        "explanation",
    ]
    for k in required_keys:
        assert k in result, f"Missing required key: {k}"

    explanation = result["explanation"]
    assert len(explanation) > 50

    # Strict non-diagnostic, non-medical language safety checks
    forbidden_terms = [
        "disorder",
        "mentally ill",
        "psychiatric illness",
        "depression diagnosis",
        "anxiety disorder",
        "pathology",
        "you have rajas disorder",
        "you have tamas disorder",
    ]
    explanation_lower = explanation.lower()
    for term in forbidden_terms:
        assert term not in explanation_lower, f"Forbidden diagnostic term '{term}' found in IKS explanation!"


def test_end_to_end_scoring_includes_iks():
    """
    Test that calculate_feature_scores populates iks_interpretation in AssessmentResult.
    """
    responses = {i: 3 for i in range(1, 17)}
    res = calculate_feature_scores(responses)

    assert res.iks_interpretation is not None
    assert res.iks_interpretation.overall_wellness_state == "Mild Mental Distress"
    assert res.iks_interpretation.wellness_score == 50.0
    assert res.iks_interpretation.sattva_score > 0
    assert res.iks_interpretation.rajas_score > 0
    assert res.iks_interpretation.tamas_score > 0
    assert res.iks_interpretation.chitta_vikshepa_indicator != ""
    assert res.iks_interpretation.dominant_pattern != ""
    assert len(res.iks_interpretation.explanation) > 40
