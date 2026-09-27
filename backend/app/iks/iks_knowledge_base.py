"""
IKS (Indian Knowledge Systems) Knowledge Base
Contains classical conceptual frameworks from Sāṁkhya, Yoga Sūtras, and the Bhagavad Gītā.
Provides educational definitions, philosophical context, and a curated library of safe, non-medical wellness practices.
"""
from typing import Dict, List, Any

IKS_DISCLAIMER = (
    "In Indian Psychology, concepts such as Triguna and Chitta Vikṣepa represent "
    "dynamic states of consciousness and mental tendencies, not static or pathological medical categories."
)

GUNA_DESCRIPTIONS: Dict[str, Dict[str, Any]] = {
    "sattva": {
        "title": "Sattva (सत्त्व)",
        "meaning": "Purity, light, harmony, clarity and steadiness",
        "qualities": ["Prakāśa (luminosity/clarity)", "Sukha (peace/well-being)", "Lāghava (mental lightness)"],
        "behavioral_manifestations": [
            "Emotional calmness and equanimity",
            "Clear and unclouded thinking",
            "Natural capacity for focus and self-observation",
            "Stable circadian routine and wholesome habits",
        ],
        "classical_reference": "Bhagavad Gītā 14.6: 'tatra sattvaṁ nirmalatvāt prakāśakam anāmayam' (Sattva is luminous and serene on account of its purity)",
    },
    "rajas": {
        "title": "Rajas (रजस्)",
        "meaning": "Movement, passion, agitation, ambition and restlessness",
        "qualities": ["Calatva (restless movement)", "Upastambhaka (stimulating/driving)", "Rāga (intense attachment/craving)"],
        "behavioral_manifestations": [
            "Mental restlessness and looping thoughts",
            "Emotional reactivity and impatience",
            "Difficulty quieting the mind before sleep",
            "Feeling mentally pressured or overwhelmed",
        ],
        "classical_reference": "Bhagavad Gītā 14.7: 'rajo rāgātmakaṁ viddhi tṛṣṇā-saṅga-samudbhavam' (Rajas is of the nature of passion, arising from craving and agitation)",
    },
    "tamas": {
        "title": "Tamas (तमस्)",
        "meaning": "Inertia, darkness, heaviness, dullness and obstruction",
        "qualities": ["Guru (heavy/lethargic)", "Varaṇaka (veiling/obscuring)", "Ālasya (inactivity/sluggishness)"],
        "behavioral_manifestations": [
            "Physical and mental heaviness or low energy",
            "Low enthusiasm or difficulty initiating tasks",
            "Disrupted sleep schedule and irregularity",
            "Mental fog or dullness",
        ],
        "classical_reference": "Bhagavad Gītā 14.8: 'tamas tv ajñāna-jaṁ viddhi mohanaṁ sarva-dehinām' (Tamas causes inertia, negligence, and lack of clarity)",
    },
}

CHITTA_VIKSHEPA_CONCEPT = {
    "title": "Chitta Vikṣepa (चित्त-विक्षेप)",
    "meaning": "Mental distractions and disturbances that scatter one's attention and peace",
    "classical_reference": "Patañjali Yoga Sūtras 1.30–1.31: Obstacles causing mental dissipation include languor (styāna), doubt (saṁśaya), carelessness (pramāda), and restlessness (alabdha-bhūmikatva).",
    "counterparts": {
        "abhyasa": "Abhyāsa (अभ्यास) — Consistent and patient daily practice",
        "vairagya": "Vairāgya (वैराग्य) — Cultivating healthy detachment from obsessive thought patterns",
        "pranayama": "Prāṇāyāma (प्राणायाम) — Regulated breathwork to steady the mind",
        "sakshi_bhava": "Sākṣī Bhāva (साक्षी भाव) — Non-judgmental self-observation",
    },
}

# Curated, deterministic recommendation knowledge base
# Structured across 9 core Indian Psychology / wellness dimensions
CURATED_RECOMMENDATIONS: List[Dict[str, Any]] = [
    # 1. Pranayama / Breathing practice
    {
        "id": "pranayama_nadi_shodhana",
        "title": "Nāḍī Śodhana (Alternate Nostril Breathing)",
        "explanation": "Sit comfortably with your spine upright. Gently close your right nostril with your thumb and inhale smoothly through the left, then switch to exhale through the right. Repeat in a calm, unhurried cadence.",
        "why_it_may_help": "This practice helps balance left and right nostril airflows (Iḍā and Piṅgalā), down-regulating mental restlessness and calming an overactive sympathetic nervous system.",
        "suggested_duration": "5–7 minutes",
        "frequency": "Once or twice daily, especially before beginning focused work or before sleep",
        "iks_concept": "Prāṇāyāma / Nadi Shodhana",
        "category": "Pranayama / breathing practice",
        "target_gunas": ["rajas"],
        "trigger_conditions": ["high_restlessness", "high_overwhelm", "elevated_vikshepa"],
    },
    {
        "id": "pranayama_bhramari",
        "title": "Bhrāmarī Prāṇāyāma (Humming Bee Breath)",
        "explanation": "Gently rest your fingers over your eyelids and ears. Inhale deeply, and upon exhalation, make a smooth, low-pitched humming sound from the throat like a soft bee.",
        "why_it_may_help": "The internal acoustic vibrations stimulate parasympathetic tone, soothing immediate emotional irritation, frustration, and sensory overstimulation.",
        "suggested_duration": "3–5 minutes (6 to 8 breath cycles)",
        "frequency": "Whenever feeling sudden irritation or emotional reactivity",
        "iks_concept": "Prāṇāyāma / Shanti",
        "category": "Emotional regulation practices",
        "target_gunas": ["rajas"],
        "trigger_conditions": ["high_reactivity", "high_restlessness"],
    },
    {
        "id": "pranayama_dirgha",
        "title": "Dīrgha Prāṇāyāma (Three-Part Vitalizing Breath)",
        "explanation": "Slowly expand the lower abdomen, then the middle ribcage, and finally the upper chest on inhalation. Exhale completely in reverse order with gentle control.",
        "why_it_may_help": "Increases oxygen saturation and vital energy (prāṇa), helping awaken physical vitality and dispelling morning sluggishness or inertia.",
        "suggested_duration": "5 minutes",
        "frequency": "Every morning upon waking or during afternoon dips in energy",
        "iks_concept": "Prāṇāyāma / Prana",
        "category": "Pranayama / breathing practice",
        "target_gunas": ["tamas"],
        "trigger_conditions": ["low_energy", "low_motivation"],
    },

    # 2. Dhyana / Meditation & Focus
    {
        "id": "dhyana_anapana",
        "title": "Mindful Breath Awareness (Ānāpāna / Dhyāna)",
        "explanation": "Rest comfortably and anchor your attention purely on the tactile sensation of incoming and outgoing breath at the tip of the nostrils or upper lip without attempting to change it.",
        "why_it_may_help": "Cultivates ekāgratā (one-pointed focus) and trains the mind to disengage gently from intrusive thought spirals without frustration.",
        "suggested_duration": "7–10 minutes",
        "frequency": "Daily in the morning or early evening",
        "iks_concept": "Dhyāna / Ekāgratā",
        "category": "Dhyana / meditation",
        "target_gunas": ["sattva", "rajas"],
        "trigger_conditions": ["poor_concentration", "moderate_distress", "sattva_dominant"],
    },
    {
        "id": "yoga_nidra_short",
        "title": "Gentle Body Sweep (Kāya Sthairyam / Mini Yoga Nidra)",
        "explanation": "Lie flat on your back or recline comfortably. Slowly rotate your mental awareness sequentially through different body parts (toes, legs, abdomen, hands, face), systematically releasing physical holding.",
        "why_it_may_help": "Facilitates pratyāhāra (sensory inward turning), providing deep physiological rest and releasing chronic neuromuscular tension.",
        "suggested_duration": "10–12 minutes",
        "frequency": "Midday rest or before retiring for the night",
        "iks_concept": "Pratyāhāra / Yoga Nidra",
        "category": "Sleep and routine improvement",
        "target_gunas": ["rajas", "tamas"],
        "trigger_conditions": ["high_overwhelm", "elevated_vikshepa", "disrupted_routine"],
    },

    # 3. Gentle Yoga & Movement
    {
        "id": "movement_sukshma_vyayama",
        "title": "Sūkṣma Vyāyāma (Gentle Conscious Joint Movements)",
        "explanation": "Perform gentle, coordinated joint rotations for the neck, shoulders, wrists, ankles, and spine synchronized with conscious, deep inhalation and exhalation.",
        "why_it_may_help": "Stimulates circulation, releases stagnation (āma) and physical heaviness, helping transition the body from dull Tamas to active clarity.",
        "suggested_duration": "8–10 minutes",
        "frequency": "Daily morning or whenever feeling physically lethargic",
        "iks_concept": "Sūkṣma Vyāyāma / Āsana",
        "category": "Gentle yoga / movement",
        "target_gunas": ["tamas"],
        "trigger_conditions": ["low_energy", "low_routine"],
    },

    # 4. Dinacharya / Daily Routine
    {
        "id": "dinacharya_morning_sunlight",
        "title": "Morning Grounding & Sunlight (Dinacaryā Anchor)",
        "explanation": "Wake at a consistent morning hour, drink a glass of warm water, and spend 5–10 minutes in natural morning sunlight while taking slow, deep breaths.",
        "why_it_may_help": "Aligns circadian rhythms with natural diurnal cycles (sūrya darśana), clearing sleep inertia and establishing a stable foundation for the day.",
        "suggested_duration": "10–15 minutes",
        "frequency": "Daily upon waking",
        "iks_concept": "Dinacaryā / Sūrya Darśana",
        "category": "Dinacharya / daily routine",
        "target_gunas": ["tamas", "sattva"],
        "trigger_conditions": ["disrupted_routine", "low_energy", "tamas_dominant"],
    },
    {
        "id": "dinacharya_evening_winddown",
        "title": "Evening Digital Fast & Wind-Down (Nidrā Sthāpanā)",
        "explanation": "Turn off digital screens 45 minutes before sleep, dim harsh lighting, and replace stimulation with calm reading, listening to soothing acoustic sounds, or gentle reflection.",
        "why_it_may_help": "Signifies to the mind that the active Rajasic phase of the day has concluded, allowing natural melatonin production and deep restorative sleep.",
        "suggested_duration": "30–45 minutes before bed",
        "frequency": "Every evening",
        "iks_concept": "Dinacaryā / Nidrā",
        "category": "Sleep and routine improvement",
        "target_gunas": ["rajas"],
        "trigger_conditions": ["high_restlessness", "disrupted_routine"],
    },

    # 5. Reflection / Self-Observation (Sakshi Bhava)
    {
        "id": "reflection_sakshi_bhava",
        "title": "The Witness Attitude (Sākṣī Bhāva Reflection)",
        "explanation": "When encountering emotional frustration, pause for 3 slow breaths. Mentally observe the rising feeling without reacting or self-judgment, noting 'I am the observer of this emotion, not the emotion itself.'",
        "why_it_may_help": "Creates mindful metacognitive space between emotional impulse and action, diffusing impulsive reactivity and fostering emotional maturity.",
        "suggested_duration": "3–5 minutes",
        "frequency": "Once daily or in moments of emotional agitation",
        "iks_concept": "Sākṣī Bhāva (साक्षी भाव)",
        "category": "Reflection / self-observation",
        "target_gunas": ["rajas", "sattva"],
        "trigger_conditions": ["high_reactivity", "moderate_distress"],
    },

    # 6. Bhagavad Gita Philosophical Reflection
    {
        "id": "philosophy_samatvam",
        "title": "Equanimity in Everyday Action (Samatvaṁ Yoga)",
        "explanation": "Reflect upon Bhagavad Gītā 2.48: 'samatvaṁ yoga ucyate' (Equanimity is yoga). Concentrate wholeheartedly on doing your present duty with care, while consciously letting go of compulsive anxiety about the end results.",
        "why_it_may_help": "Reduces chronic anticipatory worry and outcome anxiety by anchoring psychological attention in immediate, actionable effort.",
        "suggested_duration": "5 minutes of quiet contemplation",
        "frequency": "Daily before undertaking demanding projects or tasks",
        "iks_concept": "Samatvam (समत्वम्) / Karma Yoga",
        "category": "Bhagavad Gita-inspired philosophical reflection",
        "target_gunas": ["rajas", "sattva"],
        "trigger_conditions": ["high_overwhelm", "elevated_vikshepa", "moderate_distress"],
    },
    {
        "id": "philosophy_yuktahara",
        "title": "Balanced Moderation (Yuktāhāra-Vihāra)",
        "explanation": "Reflect on Bhagavad Gītā 6.16–17: Yoga is balance for one who is moderate in eating, recreation, work, and sleep. Avoid swinging between intense over-exertion and sudden burnout.",
        "why_it_may_help": "Encourages sustainable lifestyle equilibrium, preventing cycles of exhaustion and building steady resilience over time.",
        "suggested_duration": "Ongoing mindful awareness",
        "frequency": "Throughout the day",
        "iks_concept": "Yuktāhāra-Vihāra (युक्ताहारविहार)",
        "category": "Dinacharya / daily routine",
        "target_gunas": ["rajas", "tamas"],
        "trigger_conditions": ["disrupted_routine", "low_energy", "high_overwhelm"],
    },
    {
        "id": "abhyasa_swadhyaya",
        "title": "Consistent Self-Study & Practice (Svādhyāya & Abhyāsa)",
        "explanation": "Reserve 10 minutes of uninterrupted time each day to read uplifting, reflective philosophical literature or practice quiet contemplation.",
        "why_it_may_help": "Deepens existing mental equilibrium, reinforces positive cognitive habits (saṁskāras), and safeguards the mind against external turbulence.",
        "suggested_duration": "10–15 minutes",
        "frequency": "Daily",
        "iks_concept": "Svādhyāya / Abhyāsa",
        "category": "Focus practices",
        "target_gunas": ["sattva"],
        "trigger_conditions": ["sattva_dominant", "balanced_state"],
    },
]

# Map recommendations by ID for fast lookup
RECOMMENDATIONS_BY_ID = {r["id"]: r for r in CURATED_RECOMMENDATIONS}
