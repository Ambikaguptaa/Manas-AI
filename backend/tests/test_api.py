"""
API Integration and Health Check Tests
"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "Manas" in data["message"] or "Indian Psychology" in data["message"]
    assert "disclaimer" in data


def test_health_check_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "version" in data
    assert "timestamp" in data
    assert "disclaimer" in data


def test_post_assessment_with_list_input():
    """
    Test POST /api/assessment with list of 16 integer responses.
    Verifies all required fields per specification:
    assessment_id, wellness_score, wellness_state, ml_prediction, confidence,
    features, sattva_score, rajas_score, tamas_score, chitta_vikshepa_indicator,
    dominant_pattern, interpretation, recommendations, disclaimer.
    """
    payload = {
        "responses": [3] * 16
    }
    response = client.post("/api/assessment", json=payload)
    assert response.status_code == 200
    data = response.json()

    # Verify all required top-level fields
    assert "assessment_id" in data
    assert data["assessment_id"].startswith("mwa_")
    assert "wellness_score" in data
    assert data["wellness_score"] == 50.0
    assert "wellness_state" in data
    assert "ml_prediction" in data
    assert "confidence" in data
    assert isinstance(data["confidence"], float)

    # Verify features dictionary
    assert "features" in data
    features = data["features"]
    expected_dims = [
        "restlessness", "emotional_reactivity", "motivation", "energy",
        "concentration", "calmness", "routine", "overwhelm", "mental_clarity"
    ]
    for dim in expected_dims:
        assert dim in features
        assert 1.0 <= features[dim] <= 5.0

    # Verify IKS fields
    assert "sattva_score" in data
    assert "rajas_score" in data
    assert "tamas_score" in data
    assert "chitta_vikshepa_indicator" in data
    assert "dominant_pattern" in data
    assert "interpretation" in data
    assert len(data["interpretation"]) > 20

    # Verify recommendations
    assert "recommendations" in data
    assert 3 <= len(data["recommendations"]) <= 5
    for rec in data["recommendations"]:
        assert "title" in rec
        assert "explanation" in rec
        assert "why_it_may_help" in rec
        assert "suggested_duration" in rec
        assert "frequency" in rec
        assert "iks_concept" in rec

    # Verify disclaimer
    assert "disclaimer" in data
    assert "not a medical or psychiatric diagnosis" in data["disclaimer"]


def test_post_assessment_with_dict_input():
    """
    Test POST /api/assessment with dict format { "1": 4, "2": 4, ... }
    """
    payload = {
        "responses": {str(i): 4 for i in range(1, 17)}
    }
    response = client.post("/api/assessment", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "assessment_id" in data
    assert "wellness_score" in data


def test_post_assessment_validation_missing_questions():
    """
    Missing responses should return HTTP 400 or 422 with clear error message.
    """
    # Only 10 responses provided
    payload = {
        "responses": [3] * 10
    }
    response = client.post("/api/assessment", json=payload)
    assert response.status_code in [400, 422]

    # Incomplete dictionary
    dict_payload = {
        "responses": {str(i): 3 for i in range(1, 10)}
    }
    res2 = client.post("/api/assessment", json=dict_payload)
    assert res2.status_code in [400, 422]


def test_post_assessment_validation_invalid_scores():
    """
    Scores out of range 1-5 should return HTTP 400 or 422.
    """
    # Score 7 is invalid
    payload = {
        "responses": [3] * 15 + [7]
    }
    response = client.post("/api/assessment", json=payload)
    assert response.status_code in [400, 422]

    # Score 0 is invalid
    payload2 = {
        "responses": [0] + [3] * 15
    }
    res2 = client.post("/api/assessment", json=payload2)
    assert res2.status_code in [400, 422]


def test_non_diagnostic_language_guardrails():
    """
    Ensure the returned interpretation contains no psychiatric disorder diagnoses.
    """
    payload = {
        "responses": [5] * 16
    }
    response = client.post("/api/assessment", json=payload)
    assert response.status_code == 200
    data = response.json()
    interp = data["interpretation"].lower()
    assert "diagnosed with" not in interp
    assert "bipolar" not in interp
    assert "schizophrenia" not in interp
    assert "this treatment will cure" not in interp
    assert "this proves that" not in interp
