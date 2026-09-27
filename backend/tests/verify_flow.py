import json
import urllib.request
import urllib.error
import sys

sys.stdout.reconfigure(encoding='utf-8')

BASE = "http://127.0.0.1:8000/api"

def run_integration_verification():
    print("=== MANAS AI: COMPLETE END-TO-END INTEGRATION TEST ===")

    # Step 1: Health Check
    health_url = f"{BASE}/health"
    with urllib.request.urlopen(health_url) as resp:
        assert resp.status == 200
        health_data = json.loads(resp.read().decode())
        print(f"[PASS] 1. Backend Health Check: status='{health_data.get('status')}', service='{health_data.get('service')}'")

    # Step 2: Fetch Questions
    questions_url = f"{BASE}/assessment/questions"
    with urllib.request.urlopen(questions_url) as resp:
        assert resp.status == 200
        q_data = json.loads(resp.read().decode())
        total_q = q_data.get("total_questions")
        assert total_q == 16
        print(f"[PASS] 2. Questionnaire Fetch: {total_q} questions retrieved successfully.")

    # Step 3: Test POST /api/assessment with list format
    assessment_url = f"{BASE}/assessment"
    payload_list = {
        "responses": [4, 4, 3, 3, 4, 2, 4, 2, 2, 3, 2, 2, 2, 3, 2, 4]
    }
    req = urllib.request.Request(
        assessment_url, 
        data=json.dumps(payload_list).encode(), 
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        res = json.loads(resp.read().decode())
        print(f"[PASS] 3. Assessment Submission (List format): 200 OK")
        print(f"       - Assessment ID: {res['assessment_id']}")
        print(f"       - Overall Wellness Score: {res['wellness_score']}%")
        print(f"       - Wellness State: {res['wellness_state']}")
        print(f"       - ML Prediction: {res['ml_prediction']} (confidence: {res['confidence']*100:.1f}%)")
        print(f"       - Sattva: {res['sattva_score']}%, Rajas: {res['rajas_score']}%, Tamas: {res['tamas_score']}%")
        print(f"       - Chitta Vikṣepa: {res['chitta_vikshepa_indicator']}")
        print(f"       - Dominant Pattern: {res['dominant_pattern']}")
        print(f"       - Features extracted (9 dimensions): {list(res['features'].keys())}")
        print(f"       - Recommendations count: {len(res['recommendations'])}")
        print(f"       - Contributing factors count: {len(res.get('contributing_factors', []))}")
        print(f"       - Safety / High distress flag: {res.get('is_high_distress')}")
        print(f"       - Disclaimer verified: {'not a medical or psychiatric diagnosis' in res['disclaimer']}")

    # Step 4: Test POST /api/assessment with dictionary format
    payload_dict = {
        "responses": {str(i): 3 for i in range(1, 17)}
    }
    req2 = urllib.request.Request(
        assessment_url, 
        data=json.dumps(payload_dict).encode(), 
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req2) as resp:
        assert resp.status == 200
        res2 = json.loads(resp.read().decode())
        print(f"[PASS] 4. Assessment Submission (Dict format): 200 OK (ID: {res2['assessment_id']})")

    # Step 5: Test Validation - Incomplete responses (Missing answers)
    bad_payload = {"responses": [3] * 10}
    bad_req = urllib.request.Request(
        assessment_url,
        data=json.dumps(bad_payload).encode(),
        headers={"Content-Type": "application/json"}
    )
    try:
        urllib.request.urlopen(bad_req)
        assert False, "Expected HTTP error for incomplete responses"
    except urllib.error.HTTPError as err:
        assert err.code in [400, 422]
        print(f"[PASS] 5. Validation Check: Incomplete input properly rejected with HTTP {err.code}")

    # Step 6: Test Validation - Out of bounds value (e.g. 7)
    invalid_payload = {"responses": [3] * 15 + [7]}
    inv_req = urllib.request.Request(
        assessment_url,
        data=json.dumps(invalid_payload).encode(),
        headers={"Content-Type": "application/json"}
    )
    try:
        urllib.request.urlopen(inv_req)
        assert False, "Expected HTTP error for out-of-bounds score"
    except urllib.error.HTTPError as err:
        assert err.code in [400, 422]
        print(f"[PASS] 6. Validation Check: Out-of-bounds score properly rejected with HTTP {err.code}")

    print("=== ALL 6 LIVE INTEGRATION CHECKS PASSED SUCCESSFULLY ===")

if __name__ == "__main__":
    run_integration_verification()
