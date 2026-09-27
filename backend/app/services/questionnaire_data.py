"""
Questionnaire Questions and Metadata Definition (Stage 2)
Carefully designed for simple self-reflection without clinical jargon or diagnostic labels.
"""
from typing import List, Dict

SCALE_OPTIONS = [
    {"value": 1, "label": "Never"},
    {"value": 2, "label": "Rarely"},
    {"value": 3, "label": "Sometimes"},
    {"value": 4, "label": "Often"},
    {"value": 5, "label": "Almost Always"},
]

QUESTIONS_DATA: List[Dict] = [
    {
        "id": 1,
        "question": "Over recent days, how often have you felt mentally restless or had trouble sitting quietly?",
        "dimension": "Mental restlessness",
        "category": "restlessness",
        "scoring_direction": "negative",
        "iks_dimension": "rajas / chitta_viksepa",
    },
    {
        "id": 2,
        "question": "How often does your mind get caught in looping thoughts or overthinking about what happened or might happen?",
        "dimension": "Overthinking",
        "category": "restlessness",
        "scoring_direction": "negative",
        "iks_dimension": "rajas / chitta_viksepa",
    },
    {
        "id": 3,
        "question": "How often do minor unexpected hiccups or comments trigger an intense emotional reaction in you?",
        "dimension": "Emotional reactivity",
        "category": "emotional_reactivity",
        "scoring_direction": "negative",
        "iks_dimension": "rajas",
    },
    {
        "id": 4,
        "question": "How often do you experience sudden feelings of irritation, annoyance, or impatience?",
        "dimension": "Anger / frustration",
        "category": "emotional_reactivity",
        "scoring_direction": "negative",
        "iks_dimension": "rajas / krodha",
    },
    {
        "id": 5,
        "question": "When trying to unwind or go to bed, how often do you struggle to quiet down your internal thoughts?",
        "dimension": "Difficulty calming the mind",
        "category": "restlessness",
        "scoring_direction": "negative",
        "iks_dimension": "rajas / chitta_viksepa",
    },
    {
        "id": 6,
        "question": "How often do you feel motivated and genuinely enthusiastic about beginning your daily tasks?",
        "dimension": "Motivation",
        "category": "motivation",
        "scoring_direction": "positive",
        "iks_dimension": "sattva / utsaha",
    },
    {
        "id": 7,
        "question": "How often do you feel heavy, sluggish, or lacking in physical and mental energy during the day?",
        "dimension": "Energy",
        "category": "energy",
        "scoring_direction": "negative",
        "iks_dimension": "tamas / alasya",
    },
    {
        "id": 8,
        "question": "How easily are you able to sustain your attention on one activity without your mind wandering off?",
        "dimension": "Concentration",
        "category": "concentration",
        "scoring_direction": "positive",
        "iks_dimension": "sattva / ekagrata",
    },
    {
        "id": 9,
        "question": "How consistent and regular are your daily sleep schedule and wake-up hours?",
        "dimension": "Sleep / routine consistency",
        "category": "routine",
        "scoring_direction": "positive",
        "iks_dimension": "dinacharya / sattva",
    },
    {
        "id": 10,
        "question": "How reliably are you able to carry out your essential daily responsibilities and healthy habits?",
        "dimension": "Ability to maintain daily activities",
        "category": "routine",
        "scoring_direction": "positive",
        "iks_dimension": "dinacharya / abhyasa",
    },
    {
        "id": 11,
        "question": "How often do you experience a genuine sense of inner calm and peacefulness during your day?",
        "dimension": "Calmness",
        "category": "calmness",
        "scoring_direction": "positive",
        "iks_dimension": "sattva / shanti",
    },
    {
        "id": 12,
        "question": "How well are you able to remain emotionally composed and balanced when faced with unexpected demands?",
        "dimension": "Emotional balance",
        "category": "calmness",
        "scoring_direction": "positive",
        "iks_dimension": "sattva / samatvam",
    },
    {
        "id": 13,
        "question": "How often do you feel that your thoughts are clear, orderly, and unclouded?",
        "dimension": "Sense of mental clarity",
        "category": "mental_clarity",
        "scoring_direction": "positive",
        "iks_dimension": "sattva / prasada",
    },
    {
        "id": 14,
        "question": "How often are you able to pause, observe your own emotional state, and choose a thoughtful response?",
        "dimension": "Self-awareness",
        "category": "mental_clarity",
        "scoring_direction": "positive",
        "iks_dimension": "sattva / sakshi_bhava",
    },
    {
        "id": 15,
        "question": "When engaged in a conversation or activity, how easily can you anchor your mind to the present moment?",
        "dimension": "Ability to focus on the present",
        "category": "concentration",
        "scoring_direction": "positive",
        "iks_dimension": "sattva / dhyana",
    },
    {
        "id": 16,
        "question": "How often do you feel that daily pressures and thoughts are piling up and becoming mentally overwhelming?",
        "dimension": "Feeling mentally overwhelmed",
        "category": "overwhelm",
        "scoring_direction": "negative",
        "iks_dimension": "rajas / chitta_viksepa",
    },
]

QUESTIONS_BY_ID = {q["id"]: q for q in QUESTIONS_DATA}
