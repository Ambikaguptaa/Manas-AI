"""
Mental State and Chitta Vikṣepa Analysis Module
Evaluates mental stability, scatteredness (Chitta Vikṣepa), and non-medical wellness state categories.
"""
from typing import Dict, Any


def evaluate_chitta_vikshepa(
    restlessness: float,
    emotional_reactivity: float,
    overwhelm: float,
    concentration: float,
    calmness: float,
) -> Dict[str, Any]:
    """
    Computes a general mental disturbance indicator related conceptually to Chitta Vikṣepa (mental scattering).
    
    Inputs:
        restlessness (1.0 - 5.0)
        emotional_reactivity (1.0 - 5.0)
        overwhelm (1.0 - 5.0)
        concentration (1.0 - 5.0; higher = better focus)
        calmness (1.0 - 5.0; higher = calmer)
        
    Returns:
        Dictionary with score (0-100), level, and conceptual interpretation.
    """
    # Scatter components: restlessness, emotional reactivity, overwhelm, lack of focus, lack of calm
    scatter_raw = (
        restlessness * 1.2
        + emotional_reactivity
        + overwhelm
        + (6.0 - concentration)
        + (6.0 - calmness)
    ) / 5.2

    # Scale 0 to 100
    vikshepa_score = round(((scatter_raw - 1.0) / 4.0) * 100.0, 1)
    vikshepa_score = max(0.0, min(100.0, vikshepa_score))

    # Categorize into descriptive conceptual levels
    if vikshepa_score < 30.0:
        level = "Minimal Disturbance"
        description = "Shānta Chitta (Steady Mind): Your thoughts are generally centered, steady, and focused with minimal inner turbulence."
    elif vikshepa_score < 55.0:
        level = "Mild Chitta Vikṣepa"
        description = "Occasional mental scattering or periodic distraction that can be gently regulated through breath awareness and short pauses."
    elif vikshepa_score < 75.0:
        level = "Moderate Chitta Vikṣepa"
        description = "Noticeable mental restlessness, overactive thought loops, and fluctuations that disrupt concentration and calm."
    else:
        level = "Elevated Chitta Vikṣepa"
        description = "High mental dissipation, frequent emotional reactivity, and significant difficulty anchoring the mind in the present."

    return {
        "score": vikshepa_score,
        "level": level,
        "description": description,
    }


def determine_overall_wellness_state(wellness_score: float) -> str:
    """
    Classifies the user's current self-reflection into a wellness orientation state.
    Strictly educational and wellness-focused; not a medical diagnostic category.
    """
    if wellness_score >= 70.0:
        return "Balanced / Stable"
    elif wellness_score >= 50.0:
        return "Mild Mental Distress"
    elif wellness_score >= 30.0:
        return "Moderate Mental Distress"
    else:
        return "High Mental Distress"
