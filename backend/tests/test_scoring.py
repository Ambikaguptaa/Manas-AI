"""
Automated Unit and Integration Tests for Questionnaire & Scoring Engine (Stage 2)
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.scoring import calculate_feature_scores
from app.services.questionnaire_data import QUESTIONS_DATA

client = TestClient(app)


def test_get_questions_endpoint():
    response = client.get("/api/assessment/questions")
    assert response.status_code == 200
    data = response.json()
    assert data["total_questions"] == 16
    assert len(data["questions"]) == 16
    assert len(data["scale_guide"]) == 5

    # Verify first question metadata schema
    q1 = data["questions"][0]
    assert q1["id"] == 1
    assert "question" in q1
    assert "dimension" in q1
    assert "category" in q1
    assert "scoring_direction" in q1
    assert "iks_dimension" in q1


def test_balanced_profile_scoring():
    """
    Test a calm, balanced archetype:
    - Negative questions (restlessness, emotional reactivity, sluggishness, overwhelm) = 1 (Never)
    - Positive questions (motivation, concentration, calmness, routine, clarity) = 5 (Almost Always)
    """
    responses = {
        1: 1,  # restlessness
        2: 1,  # overthinking
        3: 1,  # reactivity
        4: 1,  # anger/irritation
        5: 1,  # difficulty calming mind
        6: 5,  # motivation
        7: 1,  # sluggishness -> energy = 6 - 1 = 5.0
        8: 5,  # concentration
        9: 5,  # sleep routine
        10: 5, # daily habits
        11: 5, # calmness
        12: 5, # composure
        13: 5, # mental clarity
        14: 5, # self-awareness
        15: 5, # present focus
        16: 1, # overwhelm
    }

    result = calculate_feature_scores(responses)

    assert result.total_answered == 16
    assert result.feature_scores.restlessness_score == 1.0
    assert result.feature_scores.emotional_reactivity_score == 1.0
    assert result.feature_scores.motivation_score == 5.0
    assert result.feature_scores.energy_score == 5.0
    assert result.feature_scores.concentration_score == 5.0
    assert result.feature_scores.calmness_score == 5.0
    assert result.feature_scores.routine_score == 5.0
    assert result.feature_scores.overwhelm_score == 1.0
    assert result.feature_scores.mental_clarity_score == 5.0

    # Composite scores should indicate near maximum wellness
    assert result.overall_wellness_score == 100.0
    assert result.overall_distress_score == 0.0


def test_distressed_profile_scoring():
    """
    Test a high-distress archetype:
    - Negative questions = 5 (Almost Always)
    - Positive questions = 1 (Never)
    """
    responses = {
        1: 5, 2: 5, 3: 5, 4: 5, 5: 5,
        6: 1, 7: 5, 8: 1, 9: 1, 10: 1,
        11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 5,
    }

    result = calculate_feature_scores(responses)

    assert result.feature_scores.restlessness_score == 5.0
    assert result.feature_scores.emotional_reactivity_score == 5.0
    assert result.feature_scores.motivation_score == 1.0
    assert result.feature_scores.energy_score == 1.0  # 6 - 5 = 1.0
    assert result.feature_scores.calmness_score == 1.0
    assert result.feature_scores.overwhelm_score == 5.0

    assert result.overall_wellness_score == 0.0
    assert result.overall_distress_score == 100.0


def test_api_submit_validation():
    # Test submission with missing question IDs (expect 400 error)
    incomplete_responses = {1: 3, 2: 4}
    res = client.post("/api/assessment/submit", json={"responses": incomplete_responses})
    assert res.status_code == 400

    # Test submission with out-of-bounds score (e.g. 7) (expect 422 validation error)
    invalid_responses = {i: 3 for i in range(1, 17)}
    invalid_responses[1] = 7
    res2 = client.post("/api/assessment/submit", json={"responses": invalid_responses})
    assert res2.status_code == 422


def test_api_submit_success():
    valid_responses = {i: 3 for i in range(1, 17)}
    res = client.post("/api/assessment/submit", json={"responses": valid_responses})
    assert res.status_code == 200
    data = res.json()
    assert "feature_scores" in data
    assert "overall_wellness_score" in data
    assert "overall_distress_score" in data
    assert "contributing_factors" in data
    assert "is_high_distress" in data
    assert data["feature_scores"]["restlessness_score"] == 3.0
    assert data["feature_scores"]["energy_score"] == 3.0  # 6 - 3 = 3.0
    assert data["overall_wellness_score"] == 50.0
    assert data["overall_distress_score"] == 50.0
    assert isinstance(data["contributing_factors"], list)


def test_stage6_contributing_factors_and_safety_alert():
    """
    Verify Stage 6:
    1. Balanced profile produces supportive anchors and is_high_distress=False
    2. Severe distress profile produces attention_needed factors and is_high_distress=True
    """
    balanced_responses = {
        1: 1, 2: 1, 3: 1, 4: 1, 5: 1,
        6: 5, 7: 1, 8: 5, 9: 5, 10: 5,
        11: 5, 12: 5, 13: 5, 14: 5, 15: 5, 16: 1,
    }
    res_balanced = calculate_feature_scores(balanced_responses)
    assert res_balanced.is_high_distress is False
    assert len(res_balanced.contributing_factors) >= 3
    # Supportive factors should be present
    supportive = [f for f in res_balanced.contributing_factors if f.impact_type == "supportive"]
    assert len(supportive) >= 2

    # High distress profile
    distressed_responses = {
        1: 5, 2: 5, 3: 5, 4: 5, 5: 5,
        6: 1, 7: 5, 8: 1, 9: 1, 10: 1,
        11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 5,
    }
    res_distressed = calculate_feature_scores(distressed_responses)
    assert res_distressed.is_high_distress is True
    assert len(res_distressed.contributing_factors) >= 3
    attention_needed = [f for f in res_distressed.contributing_factors if f.impact_type == "attention_needed"]
    assert len(attention_needed) >= 2
