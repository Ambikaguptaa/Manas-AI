"""
Automated Unit Tests for the IKS Wellness Recommendation Engine (Stage 5)
"""
import pytest
from app.iks.recommendations import generate_recommendations, get_recommendation_triggers
from app.services.scoring import calculate_feature_scores


def test_recommendation_schema_and_count():
    """
    Verify that 3-5 recommendations are returned, each matching the 6-field schema.
    """
    recs = generate_recommendations(
        calmness_score=3.0,
        mental_clarity_score=3.0,
        concentration_score=3.0,
        routine_score=3.0,
        motivation_score=3.0,
        energy_score=3.0,
        restlessness_score=3.0,
        emotional_reactivity_score=3.0,
        overwhelm_score=3.0,
        dominant_pattern="Balanced Dynamic",
        chitta_vikshepa_indicator="Mild Chitta Vikṣepa",
        overall_wellness_score=50.0,
        max_recommendations=4,
    )

    assert 3 <= len(recs) <= 5

    required_keys = [
        "title",
        "explanation",
        "why_it_may_help",
        "suggested_duration",
        "frequency",
        "iks_concept",
    ]

    for item in recs:
        for k in required_keys:
            assert k in item, f"Missing key {k} in recommendation"
            assert isinstance(item[k], str)
            assert len(item[k]) > 0


def test_recommendations_determinism():
    """
    Guarantee that the recommendation engine is 100% deterministic:
    identical inputs must produce identical outputs in the exact same order.
    """
    inputs = dict(
        calmness_score=2.0,
        mental_clarity_score=2.5,
        concentration_score=2.0,
        routine_score=2.5,
        motivation_score=3.0,
        energy_score=3.0,
        restlessness_score=4.5,
        emotional_reactivity_score=4.2,
        overwhelm_score=4.0,
        dominant_pattern="Rajas-predominant",
        chitta_vikshepa_indicator="Elevated Chitta Vikṣepa",
        overall_wellness_score=35.0,
    )

    run_1 = generate_recommendations(**inputs)
    run_2 = generate_recommendations(**inputs)
    run_3 = generate_recommendations(**inputs)

    assert run_1 == run_2
    assert run_2 == run_3


def test_rajas_profile_personalization():
    """
    High restlessness/reactivity profile should trigger calming breathwork (Nadi Shodhana / Bhramari)
    and equanimity reflections.
    """
    recs = generate_recommendations(
        calmness_score=1.5,
        mental_clarity_score=2.0,
        concentration_score=2.0,
        routine_score=2.0,
        motivation_score=3.0,
        energy_score=3.0,
        restlessness_score=4.8,
        emotional_reactivity_score=4.5,
        overwhelm_score=4.5,
        dominant_pattern="Rajas-predominant",
        chitta_vikshepa_indicator="Elevated Chitta Vikṣepa",
        overall_wellness_score=25.0,
    )

    titles = [r["title"] for r in recs]
    concepts = [r["iks_concept"] for r in recs]

    # Must contain soothing breathwork (Pranayama)
    assert any("Śodhana" in t or "Nadi Shodhana" in t or "Bhrāmarī" in t for t in titles)
    assert any("Prāṇāyāma" in c or "Pranayama" in c for c in concepts)


def test_tamas_profile_personalization():
    """
    Sluggish, low motivation, low routine profile should trigger morning sunlight,
    movement (Sukshma Vyayama), or vitalizing breathwork.
    """
    recs = generate_recommendations(
        calmness_score=2.5,
        mental_clarity_score=2.0,
        concentration_score=2.0,
        routine_score=1.5,
        motivation_score=1.5,
        energy_score=1.5,
        restlessness_score=2.0,
        emotional_reactivity_score=2.0,
        overwhelm_score=2.5,
        dominant_pattern="Tamas-predominant",
        chitta_vikshepa_indicator="Mild Chitta Vikṣepa",
        overall_wellness_score=30.0,
    )

    titles = [r["title"] for r in recs]
    # Expect Dinacharya or movement
    assert any("Sunlight" in t or "Dinacaryā" in t or "Vyāyāma" in t or "Dīrgha" in t for t in titles)


def test_non_medical_language_compliance():
    """
    Guarantees that recommendations do NOT make curative claims, diagnose, or prescribe.
    """
    recs = generate_recommendations(
        calmness_score=1.0,
        mental_clarity_score=1.0,
        concentration_score=1.0,
        routine_score=1.0,
        motivation_score=1.0,
        energy_score=1.0,
        restlessness_score=5.0,
        emotional_reactivity_score=5.0,
        overwhelm_score=5.0,
        dominant_pattern="Rajas-predominant",
        chitta_vikshepa_indicator="Elevated Chitta Vikṣepa",
        overall_wellness_score=10.0,
    )

    forbidden_terms = [
        "cure",
        "cures",
        "prescribe",
        "medication",
        "drug",
        "clinical treatment",
        "replaces therapy",
        "mental disorder",
    ]

    for item in recs:
        combined_text = (item["title"] + " " + item["explanation"] + " " + item["why_it_may_help"]).lower()
        for term in forbidden_terms:
            assert term not in combined_text, f"Forbidden term '{term}' found in recommendation: {item['title']}"


def test_end_to_end_scoring_includes_recommendations():
    """
    Test that calculate_feature_scores generates valid recommendations in AssessmentResult.
    """
    responses = {i: 3 for i in range(1, 17)}
    res = calculate_feature_scores(responses)

    assert res.recommendations is not None
    assert 3 <= len(res.recommendations) <= 5
    first_rec = res.recommendations[0]
    assert len(first_rec.title) > 0
    assert len(first_rec.explanation) > 0
    assert len(first_rec.why_it_may_help) > 0
    assert len(first_rec.suggested_duration) > 0
    assert len(first_rec.frequency) > 0
    assert len(first_rec.iks_concept) > 0
