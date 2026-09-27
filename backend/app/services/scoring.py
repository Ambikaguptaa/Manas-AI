"""
Psychological Feature Extraction and Scoring Engine with IKS Interpretation, ML Prediction, and Recommendations (Stage 5)
Implements reverse scoring, subscale aggregation, composite wellness index calculation,
Indian Psychology (Triguna & Chitta Vikṣepa) interpretation, Random Forest ML inference,
and personalized curated wellness recommendations.
"""
from typing import Dict, Tuple, List
from app.services.questionnaire_data import QUESTIONS_DATA, QUESTIONS_BY_ID
from app.schemas.assessment import (
    FeatureScores, 
    AssessmentResult, 
    IKSInterpretation, 
    MLPredictionResult,
    WellnessRecommendation,
    ContributingFactor
)
from app.iks.interpretation import interpret_psychological_features
from app.iks.recommendations import generate_recommendations
from app.ml.predict import predict_wellness_state


def identify_contributing_factors(feature_scores: FeatureScores) -> List[ContributingFactor]:
    """
    Identifies 3 to 4 prominent internal factors influencing the user's mental wellness profile.
    Highlights both supportive psychological anchors and areas indicating active strain or need for care.
    """
    candidates = []

    # Negative direction features: higher score => strain driver
    if feature_scores.restlessness_score >= 3.2:
        candidates.append({
            "factor_name": "Mental Restlessness & Overthinking",
            "impact_type": "attention_needed",
            "score": feature_scores.restlessness_score,
            "summary": "Your responses suggest racing thoughts and difficulty quieting mental churn.",
            "dimension": "restlessness",
            "priority": feature_scores.restlessness_score - 3.0,
        })
    elif feature_scores.restlessness_score <= 2.0:
        candidates.append({
            "factor_name": "Mental Stillness",
            "impact_type": "supportive",
            "score": feature_scores.restlessness_score,
            "summary": "Your responses indicate an unhurried, peaceful mental rhythm with minimal cognitive churn.",
            "dimension": "restlessness",
            "priority": 3.0 - feature_scores.restlessness_score,
        })

    if feature_scores.overwhelm_score >= 3.2:
        candidates.append({
            "factor_name": "Mental Overwhelm & Cognitive Load",
            "impact_type": "attention_needed",
            "score": feature_scores.overwhelm_score,
            "summary": "Your responses indicate a feeling of being pressed by daily demands or accumulated mental load.",
            "dimension": "overwhelm",
            "priority": feature_scores.overwhelm_score - 3.0,
        })

    if feature_scores.emotional_reactivity_score >= 3.2:
        candidates.append({
            "factor_name": "Emotional Reactivity & Sensitivity",
            "impact_type": "attention_needed",
            "score": feature_scores.emotional_reactivity_score,
            "summary": "Your responses indicate heightened emotional sensitivity and occasional frustration under pressure.",
            "dimension": "emotional_reactivity",
            "priority": feature_scores.emotional_reactivity_score - 3.0,
        })

    # Positive direction features: higher score => supportive anchor; lower score => attention needed
    if feature_scores.calmness_score >= 3.5:
        candidates.append({
            "factor_name": "Calmness & Emotional Composure (Samatvam)",
            "impact_type": "supportive",
            "score": feature_scores.calmness_score,
            "summary": "Your inner composure and poise serve as a stabilizing anchor during daily situations.",
            "dimension": "calmness",
            "priority": feature_scores.calmness_score - 3.0,
        })
    elif feature_scores.calmness_score <= 2.5:
        candidates.append({
            "factor_name": "Difficulty Finding Inner Composure",
            "impact_type": "attention_needed",
            "score": feature_scores.calmness_score,
            "summary": "Finding quiet spaces of inner composure currently feels challenging, leaving the mind tense.",
            "dimension": "calmness",
            "priority": 3.0 - feature_scores.calmness_score,
        })

    if feature_scores.routine_score >= 3.5:
        candidates.append({
            "factor_name": "Sleep Regularity & Daily Routine (Dinacharya)",
            "impact_type": "supportive",
            "score": feature_scores.routine_score,
            "summary": "Your regular sleep habits and structured rhythm provide grounding physical and mental support.",
            "dimension": "routine",
            "priority": feature_scores.routine_score - 3.0,
        })
    elif feature_scores.routine_score <= 2.5:
        candidates.append({
            "factor_name": "Circadian & Routine Fluctuations",
            "impact_type": "attention_needed",
            "score": feature_scores.routine_score,
            "summary": "Fluctuating sleep schedules or irregular daily habits may be contributing to fatigue and restlessness.",
            "dimension": "routine",
            "priority": 3.0 - feature_scores.routine_score,
        })

    if feature_scores.mental_clarity_score >= 3.5:
        candidates.append({
            "factor_name": "Reflective Clarity & Self-Awareness (Sākṣī Bhāva)",
            "impact_type": "supportive",
            "score": feature_scores.mental_clarity_score,
            "summary": "Your capacity for self-observation enables you to notice feelings without feeling overwhelmed by them.",
            "dimension": "mental_clarity",
            "priority": feature_scores.mental_clarity_score - 3.0,
        })
    elif feature_scores.mental_clarity_score <= 2.5:
        candidates.append({
            "factor_name": "Mental Fogginess & Clouded Outlook",
            "impact_type": "attention_needed",
            "score": feature_scores.mental_clarity_score,
            "summary": "Your responses suggest temporary mental fogginess or difficulty gaining clear perspective.",
            "dimension": "mental_clarity",
            "priority": 3.0 - feature_scores.mental_clarity_score,
        })

    if feature_scores.energy_score >= 3.5:
        candidates.append({
            "factor_name": "Physical Vitality & Readiness",
            "impact_type": "supportive",
            "score": feature_scores.energy_score,
            "summary": "Your energetic alertness supports active participation in work, learning, and daily tasks.",
            "dimension": "energy",
            "priority": feature_scores.energy_score - 3.0,
        })
    elif feature_scores.energy_score <= 2.5:
        candidates.append({
            "factor_name": "Physical Fatigue & Low Vitality",
            "impact_type": "attention_needed",
            "score": feature_scores.energy_score,
            "summary": "A feeling of physical heaviness or low vitality makes initiating daily activities more taxing.",
            "dimension": "energy",
            "priority": 3.0 - feature_scores.energy_score,
        })

    if feature_scores.concentration_score >= 3.5:
        candidates.append({
            "factor_name": "Present-Moment Focus (Dhāraṇā)",
            "impact_type": "supportive",
            "score": feature_scores.concentration_score,
            "summary": "Your ability to remain engaged in the present moment helps prevent mental dissipation.",
            "dimension": "concentration",
            "priority": feature_scores.concentration_score - 3.0,
        })
    elif feature_scores.concentration_score <= 2.5:
        candidates.append({
            "factor_name": "Concentration Dissipation",
            "impact_type": "attention_needed",
            "score": feature_scores.concentration_score,
            "summary": "Attention scatters easily across multiple thoughts, making sustained tasks feel effortful.",
            "dimension": "concentration",
            "priority": 3.0 - feature_scores.concentration_score,
        })

    if feature_scores.motivation_score >= 3.5:
        candidates.append({
            "factor_name": "Enthusiasm & Daily Motivation",
            "impact_type": "supportive",
            "score": feature_scores.motivation_score,
            "summary": "Your positive drive and enthusiasm provide constructive momentum for personal goals.",
            "dimension": "motivation",
            "priority": feature_scores.motivation_score - 3.0,
        })
    elif feature_scores.motivation_score <= 2.5:
        candidates.append({
            "factor_name": "Reduced Motivation",
            "impact_type": "attention_needed",
            "score": feature_scores.motivation_score,
            "summary": "A temporary dip in enthusiasm makes beginning tasks feel more demanding than usual.",
            "dimension": "motivation",
            "priority": 3.0 - feature_scores.motivation_score,
        })

    # Sort candidates by priority descending (strongest deviations from neutral 3.0)
    candidates.sort(key=lambda x: x["priority"], reverse=True)

    # Ensure at least 3 factors are always presented to the user
    if len(candidates) < 3:
        defaults = [
            {
                "factor_name": "Moderate Emotional Composure (Samatvam)",
                "impact_type": "supportive",
                "score": feature_scores.calmness_score,
                "summary": "Your responses indicate an overall moderate emotional composure, balancing daily demands reasonably well.",
                "dimension": "calmness",
            },
            {
                "factor_name": "Daily Habit Rhythm (Dinacharya)",
                "impact_type": "supportive",
                "score": feature_scores.routine_score,
                "summary": "Your daily routine and sleep habits show a steady baseline rhythm that supports day-to-day stability.",
                "dimension": "routine",
            },
            {
                "factor_name": "Balanced Mental Flow",
                "impact_type": "supportive",
                "score": feature_scores.restlessness_score,
                "summary": "Cognitive restlessness and calm reflection alternate in a manageable, moderate balance.",
                "dimension": "restlessness",
            },
        ]
        for d in defaults:
            if not any(c["dimension"] == d["dimension"] for c in candidates):
                candidates.append(d)
                if len(candidates) >= 3:
                    break

    selected = candidates[:4]

    return [
        ContributingFactor(
            factor_name=item["factor_name"],
            impact_type=item["impact_type"],
            score=item["score"],
            summary=item["summary"],
            dimension=item["dimension"],
        )
        for item in selected
    ]


def calculate_feature_scores(responses: Dict[int, int]) -> AssessmentResult:
    """
    Computes standardized feature scores (1.0 - 5.0) from raw questionnaire responses.
    Applies reverse scoring where appropriate for positive and negative indicators,
    runs the Indian Psychology interpretation engine, executes Random Forest ML classification,
    and derives 3-5 curated wellness recommendations.
    """
    total_questions = len(QUESTIONS_DATA)
    if len(responses) < total_questions:
        missing = [q["id"] for q in QUESTIONS_DATA if q["id"] not in responses]
        raise ValueError(f"Incomplete assessment: missing responses for question IDs {missing}")

    # 1. Restlessness (Q1, Q2, Q5) - Negative direction: Higher = more restless
    q1 = responses[1]
    q2 = responses[2]
    q5 = responses[5]
    restlessness_score = round((q1 + q2 + q5) / 3.0, 2)

    # 2. Emotional Reactivity (Q3, Q4) - Negative direction: Higher = more reactive/irritable
    q3 = responses[3]
    q4 = responses[4]
    emotional_reactivity_score = round((q3 + q4) / 2.0, 2)

    # 3. Motivation (Q6) - Positive direction: Higher = more motivated
    motivation_score = round(float(responses[6]), 2)

    # 4. Energy & Vitality (Q7) - Q7 is sluggishness (negative), so Energy = 6 - Q7
    # Higher = higher vitality and energetic alertness
    q7 = responses[7]
    energy_score = round(float(6 - q7), 2)

    # 5. Concentration & Focus (Q8, Q15) - Positive direction: Higher = better concentration
    q8 = responses[8]
    q15 = responses[15]
    concentration_score = round((q8 + q15) / 2.0, 2)

    # 6. Calmness & Composure (Q11, Q12) - Positive direction: Higher = calmer & more balanced
    q11 = responses[11]
    q12 = responses[12]
    calmness_score = round((q11 + q12) / 2.0, 2)

    # 7. Sleep & Routine Discipline (Q9, Q10) - Positive direction: Higher = stronger consistency
    q9 = responses[9]
    q10 = responses[10]
    routine_score = round((q9 + q10) / 2.0, 2)

    # 8. Overwhelm (Q16) - Negative direction: Higher = more overwhelmed
    overwhelm_score = round(float(responses[16]), 2)

    # 9. Mental Clarity & Self-awareness (Q13, Q14) - Positive direction: Higher = clearer & mindful
    q13 = responses[13]
    q14 = responses[14]
    mental_clarity_score = round((q13 + q14) / 2.0, 2)

    feature_scores = FeatureScores(
        restlessness_score=restlessness_score,
        emotional_reactivity_score=emotional_reactivity_score,
        motivation_score=motivation_score,
        energy_score=energy_score,
        concentration_score=concentration_score,
        calmness_score=calmness_score,
        routine_score=routine_score,
        overwhelm_score=overwhelm_score,
        mental_clarity_score=mental_clarity_score,
    )

    # Calculate overall composite wellness & distress indices (0-100%)
    # Standardize all 16 items to positive polarity (1=least well, 5=most well)
    positive_polarity_sum = 0
    for q_id, q_meta in QUESTIONS_BY_ID.items():
        val = responses[q_id]
        if q_meta["scoring_direction"] == "negative":
            # Invert negative questions (1 becomes 5, 5 becomes 1)
            positive_polarity_sum += (6 - val)
        else:
            # Positive questions remain as is
            positive_polarity_sum += val

    min_possible = total_questions * 1  # 16
    max_possible = total_questions * 5  # 80
    wellness_pct = round(((positive_polarity_sum - min_possible) / (max_possible - min_possible)) * 100.0, 1)
    distress_pct = round(100.0 - wellness_pct, 1)

    # 1. Run Indian Psychology (IKS) interpretation
    iks_raw_data = interpret_psychological_features(
        calmness_score=calmness_score,
        mental_clarity_score=mental_clarity_score,
        concentration_score=concentration_score,
        routine_score=routine_score,
        motivation_score=motivation_score,
        energy_score=energy_score,
        restlessness_score=restlessness_score,
        emotional_reactivity_score=emotional_reactivity_score,
        overwhelm_score=overwhelm_score,
        overall_wellness_score=wellness_pct,
    )
    iks_interpretation = IKSInterpretation(**iks_raw_data)

    # 2. Run Machine Learning (Random Forest) classification
    ml_pred_raw = predict_wellness_state(feature_scores)
    ml_prediction = MLPredictionResult(**ml_pred_raw)

    # 3. Generate curated, personalized IKS recommendations (3-5 items)
    raw_recommendations = generate_recommendations(
        calmness_score=calmness_score,
        mental_clarity_score=mental_clarity_score,
        concentration_score=concentration_score,
        routine_score=routine_score,
        motivation_score=motivation_score,
        energy_score=energy_score,
        restlessness_score=restlessness_score,
        emotional_reactivity_score=emotional_reactivity_score,
        overwhelm_score=overwhelm_score,
        dominant_pattern=iks_interpretation.dominant_pattern,
        chitta_vikshepa_indicator=iks_interpretation.chitta_vikshepa_indicator,
        overall_wellness_score=wellness_pct,
        max_recommendations=4,
    )
    recommendations = [WellnessRecommendation(**item) for item in raw_recommendations]

    # 4. Identify main contributing factors (3-4 items)
    contributing_factors = identify_contributing_factors(feature_scores)

    # 5. Check if responses indicate severe distress / safety concern
    is_high_distress = (
        distress_pct >= 60.0
        or ml_prediction.predicted_class == 3
        or (feature_scores.overwhelm_score >= 4.0 and feature_scores.restlessness_score >= 4.0)
    )

    return AssessmentResult(
        total_answered=len(responses),
        feature_scores=feature_scores,
        overall_wellness_score=wellness_pct,
        overall_distress_score=distress_pct,
        raw_responses=responses,
        iks_interpretation=iks_interpretation,
        ml_prediction=ml_prediction,
        recommendations=recommendations,
        contributing_factors=contributing_factors,
        is_high_distress=is_high_distress,
        note="Stage 6: Final mental-wellness report engine active.",
    )
