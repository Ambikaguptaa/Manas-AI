"""
IKS Wellness Recommendation Engine (Stage 5)
Provides deterministic, explainable, and personalized non-medical lifestyle recommendations
grounded in Pranayama, Dhyana, Dinacharya, and Bhagavad Gita philosophical reflection.
"""
from typing import Dict, List, Any, Union
from app.iks.iks_knowledge_base import CURATED_RECOMMENDATIONS


def get_recommendation_triggers(
    restlessness: float,
    emotional_reactivity: float,
    overwhelm: float,
    energy: float,
    motivation: float,
    routine: float,
    concentration: float,
    calmness: float,
    dominant_pattern: str,
    chitta_vikshepa_indicator: str,
    overall_wellness_score: float,
) -> set:
    """
    Identifies active psychological and IKS trigger flags based on feature scores.
    Deterministic rule-based trigger identification.
    """
    triggers = set()

    if restlessness >= 3.0:
        triggers.add("high_restlessness")
    if emotional_reactivity >= 3.0:
        triggers.add("high_reactivity")
    if overwhelm >= 3.0:
        triggers.add("high_overwhelm")
    if energy <= 2.8:
        triggers.add("low_energy")
    if motivation <= 2.8:
        triggers.add("low_motivation")
    if routine <= 2.8:
        triggers.add("disrupted_routine")
    if concentration <= 2.8:
        triggers.add("poor_concentration")
    if calmness <= 2.8:
        triggers.add("low_calmness")

    if "Elevated" in chitta_vikshepa_indicator or "Moderate" in chitta_vikshepa_indicator:
        triggers.add("elevated_vikshepa")

    if "Sattva" in dominant_pattern:
        triggers.add("sattva_dominant")
    if "Rajas" in dominant_pattern:
        triggers.add("rajas_dominant")
    if "Tamas" in dominant_pattern:
        triggers.add("tamas_dominant")

    if overall_wellness_score >= 70.0:
        triggers.add("balanced_state")
    elif overall_wellness_score <= 40.0:
        triggers.add("high_distress_state")

    return triggers


def generate_recommendations(
    calmness_score: float,
    mental_clarity_score: float,
    concentration_score: float,
    routine_score: float,
    motivation_score: float,
    energy_score: float,
    restlessness_score: float,
    emotional_reactivity_score: float,
    overwhelm_score: float,
    dominant_pattern: str,
    chitta_vikshepa_indicator: str,
    overall_wellness_score: float,
    max_recommendations: int = 4,
) -> List[Dict[str, str]]:
    """
    Generates 3 to 5 prioritized, explainable wellness recommendations from the curated knowledge base.
    
    Guarantees:
    - Pure, deterministic output: Same inputs always yield the same recommendations in identical order.
    - Diversity across categories: Balances breathwork (Pranayama), routine (Dinacharya), and reflection.
    - Strict non-medical phrasing.
    
    Each returned recommendation matches:
    {
        "title": str,
        "explanation": str,
        "why_it_may_help": str,
        "suggested_duration": str,
        "frequency": str,
        "iks_concept": str
    }
    """
    active_triggers = get_recommendation_triggers(
        restlessness=restlessness_score,
        emotional_reactivity=emotional_reactivity_score,
        overwhelm=overwhelm_score,
        energy=energy_score,
        motivation=motivation_score,
        routine=routine_score,
        concentration=concentration_score,
        calmness=calmness_score,
        dominant_pattern=dominant_pattern,
        chitta_vikshepa_indicator=chitta_vikshepa_indicator,
        overall_wellness_score=overall_wellness_score,
    )

    scored_candidates = []

    for item in CURATED_RECOMMENDATIONS:
        score = 0.0

        # Match trigger conditions
        matched_triggers = [t for t in item.get("trigger_conditions", []) if t in active_triggers]
        score += len(matched_triggers) * 25.0

        # Guna alignment
        target_gunas = item.get("target_gunas", [])
        if "rajas_dominant" in active_triggers and "rajas" in target_gunas:
            score += 30.0
        if "tamas_dominant" in active_triggers and "tamas" in target_gunas:
            score += 30.0
        if "sattva_dominant" in active_triggers and "sattva" in target_gunas:
            score += 30.0

        # High-leverage core balancing adjustments
        if "high_restlessness" in active_triggers and item["id"] == "pranayama_nadi_shodhana":
            score += 20.0
        if "high_reactivity" in active_triggers and item["id"] == "pranayama_bhramari":
            score += 20.0
        if ("low_energy" in active_triggers or "disrupted_routine" in active_triggers) and item["id"] == "dinacharya_morning_sunlight":
            score += 20.0
        if "high_overwhelm" in active_triggers and item["id"] == "philosophy_samatvam":
            score += 15.0
        if "balanced_state" in active_triggers and item["id"] == "abhyasa_swadhyaya":
            score += 25.0

        scored_candidates.append((score, item))

    # Deterministic sort: Primary key is score descending, secondary key is item ID ascending
    scored_candidates.sort(key=lambda pair: (-pair[0], pair[1]["id"]))

    # Select top 3 to 5 unique recommendations with category diversity
    selected_items = []
    seen_categories = set()

    # Pass 1: Select top scoring items with distinct categories
    for score, item in scored_candidates:
        category = item.get("category", "")
        if category not in seen_categories:
            selected_items.append(item)
            seen_categories.add(category)
        if len(selected_items) >= max_recommendations:
            break

    # Pass 2: Fill up to max_recommendations if needed
    if len(selected_items) < max_recommendations:
        for score, item in scored_candidates:
            if item not in selected_items:
                selected_items.append(item)
            if len(selected_items) >= max_recommendations:
                break

    # Format into required output schema
    formatted_recommendations = []
    for item in selected_items:
        formatted_recommendations.append({
            "title": item["title"],
            "explanation": item["explanation"],
            "why_it_may_help": item["why_it_may_help"],
            "suggested_duration": item["suggested_duration"],
            "frequency": item["frequency"],
            "iks_concept": item["iks_concept"],
        })

    return formatted_recommendations
