"""
IKS Interpretation Engine (Stage 3)
Translates psychological feature scores into accessible, respectful Indian Psychology insights.
Provides educational reflections without medical diagnoses.
"""
from typing import Dict, Any
from app.iks.guna_analysis import calculate_guna_tendencies
from app.iks.mental_state import evaluate_chitta_vikshepa, determine_overall_wellness_state
from app.iks.iks_knowledge_base import GUNA_DESCRIPTIONS, CHITTA_VIKSHEPA_CONCEPT


def generate_iks_explanation(
    overall_wellness_state: str,
    dominant_pattern: str,
    sattva: float,
    rajas: float,
    tamas: float,
    vikshepa_data: Dict[str, Any],
    restlessness: float,
    calmness: float,
    energy: float,
    routine: float,
) -> str:
    """
    Constructs an accessible, non-diagnostic explanation synthesizing Triguna and Chitta Vikṣepa.
    Follows compassionate, academic language guidelines.
    """
    paragraphs = []

    # 1. Observation of current mental-emotional dynamics
    if sattva >= 65.0 and rajas < 40.0 and tamas < 40.0:
        obs = (
            "Your responses indicate a strong foundation of mental calmness, inner clarity, and emotional balance. "
            "You report steady focus during daily activities and a generally restful rhythm of thought."
        )
    elif rajas >= 55.0 and rajas >= tamas:
        obs = (
            "Your responses indicate relatively strong mental restlessness, overthinking, and some difficulty calming the mind. "
            "You may be experiencing rapid internal thoughts, emotional impatience, or a feeling of being pressed by daily demands."
        )
    elif tamas >= 55.0 and tamas > rajas:
        obs = (
            "Your responses suggest a predominant experience of low energy, sluggishness, and reduced enthusiasm for daily routines. "
            "There may be a sense of physical heaviness, hesitation to begin activities, or an irregular sleep pattern."
        )
    elif rajas >= 45.0 and tamas >= 45.0:
        obs = (
            "Your responses reflect a dual tendency of mental overactivity coupled with periods of fatigue and low vitality. "
            "This often manifests as racing thoughts while feeling physically drained or finding it difficult to maintain a steady schedule."
        )
    else:
        obs = (
            "Your responses reflect a moderate, fluctuating state where moments of mental composure alternate with periodic "
            "distraction, mild stress, or temporary fatigue."
        )
    paragraphs.append(obs)

    # 2. Indian Psychology contextualization (Triguna & Chitta Vikṣepa)
    iks_ctx = []
    if "Sattva" in dominant_pattern:
        iks_ctx.append(
            f"In the framework of Indian Psychology, this state aligns with a predominant expression of Sattva ({sattva}%), "
            "characterized by clarity (prakāśa), serenity (sukha), and cognitive lightness."
        )
    elif "Rajas" in dominant_pattern:
        iks_ctx.append(
            f"In the context of Indian Psychology, this pattern can be discussed in relation to an elevation of Rajas ({rajas}%), "
            "which represents movement, restlessness (calatva), and emotional reactivity."
        )
    elif "Tamas" in dominant_pattern:
        iks_ctx.append(
            f"In the context of Indian Psychology, this pattern relates to an increased presence of Tamas ({tamas}%), "
            "which manifests as inertia (ālasya), mental dullness, and heaviness (guru)."
        )
    else:
        iks_ctx.append(
            f"In Indian Psychology, your current profile reflects a dynamic interplay among Sattva ({sattva}%), Rajas ({rajas}%), "
            f"and Tamas ({tamas}%)."
        )

    # Add Chitta Vikṣepa perspective
    vik_level = vikshepa_data["level"]
    if "Minimal" in vik_level:
        iks_ctx.append(
            "Your mental disturbance indicator indicates Shānta Chitta (a steady mind), reflecting minimal mental scattering (Chitta Vikṣepa) "
            "and natural present-moment grounding."
        )
    elif "Mild" in vik_level:
        iks_ctx.append(
            "The assessment suggests mild Chitta Vikṣepa (occasional mental dissipation), where thoughts periodically drift but remain relatively easy to refocus."
        )
    else:
        iks_ctx.append(
            f"The assessment points to {vik_level.lower()} (disturbances of the mind), where the mind's attention feels dissipated across competing worries or overactive loops."
        )

    paragraphs.append(" ".join(iks_ctx))

    # 3. Constructive, lifestyle-oriented suggestions based on IKS
    suggestions = []
    if rajas >= 50.0:
        suggestions.append("soothing breath regulation (such as Nadi Shodhana / Anulom Vilom prāṇāyāma) to steady excessive mental motion")
    if tamas >= 50.0 or routine <= 2.5:
        suggestions.append("establishing a disciplined circadian routine (dinacharya) with regular wake-up hours, exposure to morning sunlight, and wholesome activity")
    if calmness <= 3.0 or sattva < 50.0:
        suggestions.append("cultivating mindful self-observation (sākṣī bhāva) and gentle meditation (dhyāna) to untangle from looping thoughts")
    if not suggestions:
        suggestions.append("maintaining your healthy daily practices (abhyāsa) and reinforcing balanced moderation (samatvam)")

    rec_text = (
        f"To nurture natural equilibrium, traditional IKS principles recommend {', '.join(suggestions)}. "
        "In Indian thought, the Gunas are dynamic qualities that shift continuously with our daily environment, routine, and conscious practice."
    )
    paragraphs.append(rec_text)

    return "\n\n".join(paragraphs)


def interpret_psychological_features(
    calmness_score: float,
    mental_clarity_score: float,
    concentration_score: float,
    routine_score: float,
    motivation_score: float,
    energy_score: float,
    restlessness_score: float,
    emotional_reactivity_score: float,
    overwhelm_score: float,
    overall_wellness_score: float,
) -> Dict[str, Any]:
    """
    Main orchestration function for Stage 3 IKS Interpretation.
    
    Transforms feature scores into:
    - overall_wellness_state
    - wellness_score
    - sattva_score, rajas_score, tamas_score
    - chitta_vikshepa_indicator
    - dominant_pattern
    - accessible explanation
    """
    # 1. Guna tendencies
    guna_data = calculate_guna_tendencies(
        calmness=calmness_score,
        mental_clarity=mental_clarity_score,
        concentration=concentration_score,
        routine=routine_score,
        motivation=motivation_score,
        energy=energy_score,
        restlessness=restlessness_score,
        emotional_reactivity=emotional_reactivity_score,
        overwhelm=overwhelm_score,
    )

    # 2. Mental state & Chitta Vikṣepa
    vikshepa_data = evaluate_chitta_vikshepa(
        restlessness=restlessness_score,
        emotional_reactivity=emotional_reactivity_score,
        overwhelm=overwhelm_score,
        concentration=concentration_score,
        calmness=calmness_score,
    )

    overall_wellness_state = determine_overall_wellness_state(overall_wellness_score)

    # 3. Generate accessible explanation
    explanation = generate_iks_explanation(
        overall_wellness_state=overall_wellness_state,
        dominant_pattern=guna_data["dominant_pattern"],
        sattva=guna_data["sattva_score"],
        rajas=guna_data["rajas_score"],
        tamas=guna_data["tamas_score"],
        vikshepa_data=vikshepa_data,
        restlessness=restlessness_score,
        calmness=calmness_score,
        energy=energy_score,
        routine=routine_score,
    )

    return {
        "overall_wellness_state": overall_wellness_state,
        "wellness_score": overall_wellness_score,
        "sattva_score": guna_data["sattva_score"],
        "rajas_score": guna_data["rajas_score"],
        "tamas_score": guna_data["tamas_score"],
        "proportions": guna_data["proportions"],
        "chitta_vikshepa_indicator": vikshepa_data["level"],
        "chitta_vikshepa_score": vikshepa_data["score"],
        "chitta_vikshepa_details": vikshepa_data["description"],
        "dominant_pattern": guna_data["dominant_pattern"],
        "explanation": explanation,
        "philosophical_context": (
            "Grounded in Sāṁkhya-Yoga psychology and the Bhagavad Gītā (Ch. 14). "
            "These conceptual tendencies reflect current states of mind that can be harmonized through conscious lifestyle and inner practice."
        ),
    }
