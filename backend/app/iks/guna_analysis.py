"""
Guna Tendency Analysis Module
Computes conceptual tendencies for Sattva, Rajas, and Tamas from standardized psychological features.
"""
from typing import Dict, Any, Tuple


def calculate_guna_tendencies(
    calmness: float,
    mental_clarity: float,
    concentration: float,
    routine: float,
    motivation: float,
    energy: float,
    restlessness: float,
    emotional_reactivity: float,
    overwhelm: float,
) -> Dict[str, Any]:
    """
    Computes Sattva, Rajas, and Tamas tendency scores (0-100 scale) and relative proportions.
    
    Inputs are feature scores on a 1.0 to 5.0 scale.
    Outputs are non-medical, conceptual wellness indicators.
    """
    # 1. Sattva Tendency: Calmness, clarity, focus, routine regularity, motivation, energy
    sattva_raw = (calmness + mental_clarity + concentration + routine + motivation + energy) / 6.0
    sattva_score = round(((sattva_raw - 1.0) / 4.0) * 100.0, 1)
    sattva_score = max(0.0, min(100.0, sattva_score))

    # 2. Rajas Tendency: Restlessness, emotional reactivity, mental overwhelm
    rajas_raw = (restlessness + emotional_reactivity + overwhelm) / 3.0
    rajas_score = round(((rajas_raw - 1.0) / 4.0) * 100.0, 1)
    rajas_score = max(0.0, min(100.0, rajas_score))

    # 3. Tamas Tendency: Low energy, low motivation, disrupted routine, mental dullness
    # Inverted from positive features: (6.0 - score)
    low_energy = 6.0 - energy
    low_motivation = 6.0 - motivation
    disrupted_routine = 6.0 - routine
    low_clarity = 6.0 - mental_clarity
    tamas_raw = (low_energy + low_motivation + disrupted_routine + low_clarity) / 4.0
    tamas_score = round(((tamas_raw - 1.0) / 4.0) * 100.0, 1)
    tamas_score = max(0.0, min(100.0, tamas_score))

    # Relative Triguna distribution (summing to 100%)
    raw_sum = sattva_raw + rajas_raw + tamas_raw
    if raw_sum > 0:
        sattva_pct = round((sattva_raw / raw_sum) * 100.0, 1)
        rajas_pct = round((rajas_raw / raw_sum) * 100.0, 1)
        tamas_pct = round(100.0 - (sattva_pct + rajas_pct), 1)
    else:
        sattva_pct, rajas_pct, tamas_pct = 33.3, 33.3, 33.4

    # Determine dominant pattern
    dominant_pattern = identify_dominant_pattern(sattva_score, rajas_score, tamas_score)

    return {
        "sattva_score": sattva_score,
        "rajas_score": rajas_score,
        "tamas_score": tamas_score,
        "proportions": {
            "sattva_percentage": sattva_pct,
            "rajas_percentage": rajas_pct,
            "tamas_percentage": tamas_pct,
        },
        "dominant_pattern": dominant_pattern,
    }


def identify_dominant_pattern(sattva: float, rajas: float, tamas: float) -> str:
    """
    Identifies the primary conceptual pattern based on relative tendency scores.
    """
    scores = {"Sattva": sattva, "Rajas": rajas, "Tamas": tamas}
    sorted_gunas = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    top_guna, top_score = sorted_gunas[0]
    second_guna, second_score = sorted_gunas[1]

    # If top two gunas are very close (within 5 points), classify as a dynamic mixed state
    if (top_score - second_score) <= 5.0 and top_score > 35.0:
        if set([top_guna, second_guna]) == {"Rajas", "Tamas"}:
            return "Rajas-Tamas mixed pattern (Active Agitation with Fatigue)"
        elif set([top_guna, second_guna]) == {"Sattva", "Rajas"}:
            return "Sattva-Rajas dynamic (Active Clarity with Restlessness)"
        elif set([top_guna, second_guna]) == {"Sattva", "Tamas"}:
            return "Sattva-Tamas dynamic (Calm with Low Energy)"
        return "Balanced Dynamic (Interplay of Gunas)"

    if top_guna == "Sattva":
        return "Sattva-predominant (Clarity, Calmness & Stability)"
    elif top_guna == "Rajas":
        return "Rajas-predominant (Restlessness & High Mental Activity)"
    else:
        return "Tamas-predominant (Inertia, Fatigue & Low Initiative)"
