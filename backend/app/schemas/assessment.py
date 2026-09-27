"""
Pydantic Schemas for Questionnaire, Assessment Scoring, IKS Interpretation, ML Prediction, and Recommendations (Stage 5)
"""
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field, field_validator


class QuestionOption(BaseModel):
    value: int = Field(..., ge=1, le=5, description="Scale value (1-5)")
    label: str = Field(..., description="Scale label (e.g. Never, Sometimes)")


class QuestionMetadata(BaseModel):
    id: int = Field(..., description="Unique question identifier")
    question: str = Field(..., description="Relatable, non-clinical question text")
    dimension: str = Field(..., description="Target psychological dimension")
    category: str = Field(..., description="Internal feature category")
    scoring_direction: str = Field(..., description="'positive' (higher = wellness) or 'negative' (higher = distress)")
    iks_dimension: str = Field(..., description="Associated IKS concept (e.g., rajas, tamas, sattva, dinacharya)")


class QuestionnaireResponse(BaseModel):
    total_questions: int
    scale_guide: List[QuestionOption]
    questions: List[QuestionMetadata]


class AssessmentSubmission(BaseModel):
    """
    Flexible User responses submission supporting:
    1. List of 16 scores: [3, 4, 2, ...]
    2. List of objects: [{"question_id": 1, "value": 3}, ...]
    3. Dict of question ID to response: {1: 3, 2: 4, ...} or {"1": 3, "2": 4, ...}
    """
    responses: Union[Dict[int, int], Dict[str, int], List[int], List[Dict[str, Any]]] = Field(
        ..., 
        description="Questionnaire responses in list or dictionary format (scale 1-5)"
    )

    @field_validator("responses")
    @classmethod
    def validate_and_normalize_responses(cls, v: Any) -> Dict[int, int]:
        if not v:
            raise ValueError("Responses cannot be empty")
        
        parsed: Dict[int, int] = {}

        if isinstance(v, list):
            if len(v) == 0:
                raise ValueError("Responses list cannot be empty")
            
            # Check if list of numbers [score_q1, score_q2, ...]
            if all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in v):
                if len(v) != 16:
                    raise ValueError(f"Incomplete assessment: expected exactly 16 responses for questions 1 to 16, but received {len(v)}.")
                for idx, score in enumerate(v, start=1):
                    val = int(score)
                    if not (1 <= val <= 5):
                        raise ValueError(f"Score for question {idx} must be between 1 and 5 (got {score})")
                    parsed[idx] = val

            # Check if list of dict objects [{"question_id": 1, "value": 3}, ...]
            elif all(isinstance(x, dict) for x in v):
                for item in v:
                    q_id = item.get("question_id") if "question_id" in item else item.get("id")
                    score = item.get("value") if "value" in item else item.get("score")
                    if q_id is None or score is None:
                        raise ValueError(f"Each response object must include 'question_id' and 'value' (got {item})")
                    try:
                        q_int = int(q_id)
                        s_int = int(score)
                    except (ValueError, TypeError):
                        raise ValueError(f"Question ID and score must be numeric (got {item})")
                    if not (1 <= s_int <= 5):
                        raise ValueError(f"Score for question {q_int} must be between 1 and 5 (got {score})")
                    parsed[q_int] = s_int
            else:
                raise ValueError("List responses must contain numbers (1-5) or question-value objects.")

        elif isinstance(v, dict):
            for k, score in v.items():
                try:
                    q_id = int(k)
                    s_int = int(score)
                except (ValueError, TypeError):
                    raise ValueError(f"Question ID and score must be numeric integers (got {k}: {score})")
                if not (1 <= s_int <= 5):
                    raise ValueError(f"Score for question {q_id} must be between 1 and 5 (got {score})")
                parsed[q_id] = s_int
        else:
            raise ValueError("Responses must be provided as a list or key-value object.")

        return parsed


class FeatureScores(BaseModel):
    """
    Standardized internal psychological feature scores (scale: 1.0 to 5.0)
    """
    restlessness_score: float = Field(..., ge=1.0, le=5.0, description="Mental restlessness & overthinking (higher = higher restlessness)")
    emotional_reactivity_score: float = Field(..., ge=1.0, le=5.0, description="Irritation & reactive emotional triggers (higher = higher reactivity)")
    motivation_score: float = Field(..., ge=1.0, le=5.0, description="Initiative & daily goal enthusiasm (higher = higher motivation)")
    energy_score: float = Field(..., ge=1.0, le=5.0, description="Vitality vs. lethargy (higher = higher energy)")
    concentration_score: float = Field(..., ge=1.0, le=5.0, description="Focus & present-moment attention (higher = better focus)")
    calmness_score: float = Field(..., ge=1.0, le=5.0, description="Inner peace & quiet mind (higher = calmer)")
    routine_score: float = Field(..., ge=1.0, le=5.0, description="Sleep & daily routine consistency (higher = better routine)")
    overwhelm_score: float = Field(..., ge=1.0, le=5.0, description="Sense of mental overload/pressure (higher = more overwhelmed)")
    mental_clarity_score: float = Field(..., ge=1.0, le=5.0, description="Clarity & mindful self-awareness (higher = clearer)")


class IKSInterpretation(BaseModel):
    """
    Interpretive Indian Psychology (IKS) assessment output.
    Strictly educational and self-reflective; not a clinical or medical diagnosis.
    """
    overall_wellness_state: str = Field(..., description="E.g. Balanced / Stable, Mild Mental Distress, etc.")
    wellness_score: float = Field(..., description="Composite wellness index (0-100)")
    sattva_score: float = Field(..., description="Sattva tendency score (0-100)")
    rajas_score: float = Field(..., description="Rajas tendency score (0-100)")
    tamas_score: float = Field(..., description="Tamas tendency score (0-100)")
    chitta_vikshepa_indicator: str = Field(..., description="Categorized level of mental disturbance/scattering")
    dominant_pattern: str = Field(..., description="Identified dominant Guna tendency pattern")
    explanation: str = Field(..., description="Accessible, compassionate, non-diagnostic narrative explanation")
    chitta_vikshepa_score: Optional[float] = None
    chitta_vikshepa_details: Optional[str] = None
    proportions: Optional[Dict[str, float]] = None
    philosophical_context: Optional[str] = None


class MLPredictionResult(BaseModel):
    """
    Machine Learning (Random Forest) pattern classification result.
    Strictly an academic classification demonstration; NOT a medical diagnosis.
    """
    predicted_class: int = Field(..., ge=0, le=3, description="Model output class (0-3)")
    predicted_label: str = Field(..., description="E.g. Balanced / Stable, High Mental Distress")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Probability of predicted class")
    class_probabilities: Dict[str, float] = Field(..., description="Complete multi-class probability distribution")
    feature_values: Dict[str, float] = Field(..., description="9 feature vector values used for inference")
    model_type: str = "RandomForestClassifier"
    disclaimer: str = (
        "Academic ML pattern classification on self-reported Likert features; not a clinical medical diagnosis."
    )


class WellnessRecommendation(BaseModel):
    """
    Curated non-medical wellness recommendation grounded in Indian Psychology.
    """
    title: str = Field(..., description="Title of the practice")
    explanation: str = Field(..., description="Practical instructions and overview")
    why_it_may_help: str = Field(..., description="Rationale in terms of mental-emotional balance")
    suggested_duration: str = Field(..., description="E.g. '5–7 minutes'")
    frequency: str = Field(..., description="E.g. 'Once or twice daily'")
    iks_concept: str = Field(..., description="Underlying IKS concept (Pranayama, Dinacharya, etc.)")


class ContributingFactor(BaseModel):
    """
    Identified internal factor influencing the user's current wellness or distress state.
    """
    factor_name: str = Field(..., description="Name of the psychological factor")
    impact_type: str = Field(..., description="'supportive' (protective strength) or 'attention_needed' (strain driver)")
    score: float = Field(..., description="Standardized score on 1.0 - 5.0 scale")
    summary: str = Field(..., description="Plain-language non-clinical interpretation of its role")
    dimension: str = Field(..., description="Internal feature dimension key")


class AssessmentResult(BaseModel):
    """
    Computed assessment output containing calculated feature scores, overall indices, IKS interpretation,
    Machine Learning model prediction, personalized IKS wellness recommendations, and main contributing factors.
    """
    total_answered: int
    feature_scores: FeatureScores
    overall_wellness_score: float = Field(..., ge=0.0, le=100.0, description="Composite positive wellness index (0-100%)")
    overall_distress_score: float = Field(..., ge=0.0, le=100.0, description="Composite mental distress index (0-100%)")
    raw_responses: Dict[int, int]
    iks_interpretation: Optional[IKSInterpretation] = None
    ml_prediction: Optional[MLPredictionResult] = None
    recommendations: Optional[List[WellnessRecommendation]] = None
    contributing_factors: Optional[List[ContributingFactor]] = None
    is_high_distress: bool = Field(default=False, description="Whether responses indicate elevated distress requiring supportive guidance")
    note: str = "Stage 6: Final mental-wellness report engine active."


class AssessmentResponse(BaseModel):
    """
    Standardized, user-facing end-to-end mental wellness assessment response.
    Encapsulates all required metrics, Indian Psychology tendencies, 
    Random Forest ML predictions, and personalized lifestyle recommendations.
    """
    assessment_id: str = Field(..., description="Unique assessment tracking identifier")
    wellness_score: float = Field(..., ge=0.0, le=100.0, description="Overall wellness score (0-100%)")
    wellness_state: str = Field(..., description="Overall mental wellness category")
    ml_prediction: str = Field(..., description="Random Forest classification label")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Model prediction confidence (0-1)")
    features: Dict[str, float] = Field(..., description="Key psychological feature scores (1.0 - 5.0)")
    sattva_score: float = Field(..., ge=0.0, le=100.0, description="Sattva tendency score")
    rajas_score: float = Field(..., ge=0.0, le=100.0, description="Rajas tendency score")
    tamas_score: float = Field(..., ge=0.0, le=100.0, description="Tamas tendency score")
    chitta_vikshepa_indicator: str = Field(..., description="Mental scattering level indicator")
    dominant_pattern: str = Field(..., description="Dominant Guna pattern description")
    interpretation: str = Field(..., description="Short, plain-language narrative interpretation")
    recommendations: List[WellnessRecommendation] = Field(..., description="3 to 5 personalized IKS wellness practices")
    disclaimer: str = Field(..., description="Non-medical self-reflection disclaimer statement")

    # Supplementary rich fields for ReportView & backward compatibility:
    overall_wellness_score: Optional[float] = None
    overall_distress_score: Optional[float] = None
    feature_scores: Optional[FeatureScores] = None
    iks_interpretation: Optional[IKSInterpretation] = None
    ml_prediction_details: Optional[MLPredictionResult] = None
    contributing_factors: Optional[List[ContributingFactor]] = None
    is_high_distress: bool = False
    note: str = "End-to-end integrated mental wellness assessment active."
