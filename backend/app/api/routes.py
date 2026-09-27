import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException
from app.config import settings
from app.services.questionnaire_data import QUESTIONS_DATA, SCALE_OPTIONS
from app.schemas.assessment import (
    QuestionnaireResponse, 
    QuestionMetadata, 
    QuestionOption,
    AssessmentSubmission, 
    AssessmentResult,
    AssessmentResponse
)
from app.services.scoring import calculate_feature_scores

router = APIRouter()


@router.get("/health")
def health_check():
    """
    Health check endpoint for system monitoring and frontend connectivity verification.
    """
    return {
        "status": "online",
        "service": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "timestamp": datetime.now().isoformat(),
        "disclaimer": settings.DISCLAIMER_TEXT,
    }


@router.get("/assessment/questions", response_model=QuestionnaireResponse)
def get_assessment_questions():
    """
    Retrieves the 16 non-clinical self-reflection questionnaire items along with metadata and scale guide.
    """
    questions = [QuestionMetadata(**q) for q in QUESTIONS_DATA]
    options = [QuestionOption(**opt) for opt in SCALE_OPTIONS]
    return QuestionnaireResponse(
        total_questions=len(questions),
        scale_guide=options,
        questions=questions,
    )


def _evaluate_and_build_response(submission: AssessmentSubmission) -> AssessmentResponse:
    """
    Internal orchestrator for complete assessment evaluation:
    1. Psychological feature extraction
    2. Composite wellness & distress index calculation
    3. Indian Psychology (Triguna & Chitta Vikṣepa) interpretation
    4. Random Forest ML pattern classification
    5. Curated personalized recommendations
    6. Main contributing factor identification
    """
    result: AssessmentResult = calculate_feature_scores(submission.responses)

    assessment_id = f"mwa_{uuid.uuid4().hex[:12]}"

    features_dict = {
        "restlessness": result.feature_scores.restlessness_score,
        "emotional_reactivity": result.feature_scores.emotional_reactivity_score,
        "motivation": result.feature_scores.motivation_score,
        "energy": result.feature_scores.energy_score,
        "concentration": result.feature_scores.concentration_score,
        "calmness": result.feature_scores.calmness_score,
        "routine": result.feature_scores.routine_score,
        "overwhelm": result.feature_scores.overwhelm_score,
        "mental_clarity": result.feature_scores.mental_clarity_score,
    }

    wellness_state = (
        result.iks_interpretation.overall_wellness_state
        if result.iks_interpretation
        else "Balanced / Stable"
    )

    ml_label = (
        result.ml_prediction.predicted_label
        if result.ml_prediction
        else wellness_state
    )

    confidence = (
        round(result.ml_prediction.confidence, 4)
        if result.ml_prediction
        else 1.0
    )

    interpretation = (
        result.iks_interpretation.explanation
        if result.iks_interpretation
        else "Your responses indicate an overall balanced state."
    )

    sattva = result.iks_interpretation.sattva_score if result.iks_interpretation else 50.0
    rajas = result.iks_interpretation.rajas_score if result.iks_interpretation else 50.0
    tamas = result.iks_interpretation.tamas_score if result.iks_interpretation else 50.0
    vikshepa = result.iks_interpretation.chitta_vikshepa_indicator if result.iks_interpretation else "Shānta Chitta"
    dominant = result.iks_interpretation.dominant_pattern if result.iks_interpretation else "Balanced"

    return AssessmentResponse(
        assessment_id=assessment_id,
        wellness_score=result.overall_wellness_score,
        wellness_state=wellness_state,
        ml_prediction=ml_label,
        confidence=confidence,
        features=features_dict,
        sattva_score=sattva,
        rajas_score=rajas,
        tamas_score=tamas,
        chitta_vikshepa_indicator=vikshepa,
        dominant_pattern=dominant,
        interpretation=interpretation,
        recommendations=result.recommendations or [],
        disclaimer="This assessment provides a wellness-oriented indication based on your responses. It is not a medical or psychiatric diagnosis.",
        # Supplementary rich attributes for UI ReportView:
        overall_wellness_score=result.overall_wellness_score,
        overall_distress_score=result.overall_distress_score,
        feature_scores=result.feature_scores,
        iks_interpretation=result.iks_interpretation,
        ml_prediction_details=result.ml_prediction,
        contributing_factors=result.contributing_factors or [],
        is_high_distress=result.is_high_distress,
        note="End-to-end integrated mental wellness assessment active.",
    )


@router.post("/assessment", response_model=AssessmentResponse)
def conduct_assessment(submission: AssessmentSubmission):
    """
    Standard End-to-End Mental Wellness Assessment Endpoint:
    Accepts user responses (in list or dictionary format), validates values, extracts features,
    applies ML classification, derives Indian Psychology insights, and returns personalized recommendations.
    """
    try:
        return _evaluate_and_build_response(submission)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating assessment: {str(e)}")


@router.post("/assessment/submit", response_model=AssessmentResponse)
def submit_assessment(submission: AssessmentSubmission):
    """
    Alias route for /assessment to ensure backward compatibility with existing tests and clients.
    """
    try:
        return _evaluate_and_build_response(submission)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating assessment: {str(e)}")

