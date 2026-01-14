"""out_temp = {
        "summary": {
            "session_type": "string",
            "presenting_concerns": "string",
            "interventions_used": "string",
            "response": "string",
            "progress_toward_goals": "string",
            "clinical_impression": "string",
            "safety_concerns": "string",
            "follow_up": "string",
            "brief_notes": "brief notes escalated to risk "
            },

        "risk_flags": [
            {
            "category": "string",
            
            "description": "string",
            "why_it_matters": "string",
            "evidence": "string",
            "severity": "high | medium | low"
            }
        ],

        "pdpm_alignment": {
            "summary": "string",
        
            "notes": "string"
        },

        "consistency_checks": {
            "adl_conflicts": "string",
            "behavior_conflicts": "string",
            "therapy_conflicts": "string",
            "pain_conflicts": "string",
            "diagnosis_alignment": "string"
        },

        "scores": {
            "documentation_quality": "25 to 95",
            "consistency_score": "25 to 95",
            "compliance_score": "25 to 95",
            "risk_level": "high (when score less then 40)| medium (when score greter then 40 and less then 75)| low (when score greter then 75)"
        }
    }
"""

out_temp = {
    "summary": {
        "session_type": {"value": "string", "score": "0–1"},
        "presenting_concerns": {"value": "string", "score": "0–1"},
        "interventions_used": {"value": "string", "score": "0–2"},
        "response": {"value": "string", "score": "0–1"},
        "progress_toward_goals": {"value": "string", "score": "0–1"},
        "clinical_impression": {"value": "string", "score": "0–1"},
        "safety_concerns": {"value": "string", "score": "0–1"},
        "follow_up": {"value": "string", "score": "0–1"},
        "brief_notes": {"value": "brief notes escalated to risk", "score": "0–0.5"}  # unchanged
    },

    "risk_flags": [
        {
            "category": {"value": "string", "score": "0–1"},
            "description": {"value": "string", "score": "0–1"},
            "why_it_matters": {"value": "string", "score": "0–1"},
            "evidence": {"value": "string", "score": "0–2"},
            "severity": {"value": "high | medium | low", "score": "low=0.3 | medium=0.6 | high=0.9"}
        }
    ],

    "pdpm_alignment": {
        "summary": {"value": "string", "score": "0–0.5"},   
        "notes": {"value": "string", "score": "0–0.5"}     
    },

    "consistency_checks": {
        "adl_conflicts": {"value": "string", "score": "0.2–1"},
        "behavior_conflicts": {"value": "string", "score": "0.2–1"},
        "therapy_conflicts": {"value": "string", "score": "0.2–1"},
        "pain_conflicts": {"value": "string", "score": "0.2–1"},
        "diagnosis_alignment": {"value": "string", "score": "0.2–1"}
    }
}



score_rules = """
    DETERMINISTIC SCORING RULES

    Documentation Quality (45–90):
    Base 60
    +5 each if present: session_type, presenting_concerns, interventions_used,
    response, progress_toward_goals, follow_up
    -5 if 2+ summary fields = "Not documented"
    -5 if brief_notes vague
    -10 if summary text largely duplicated

    Consistency (50–85):
    Base 75
    -10 per conflict: ADL, behavior, therapy, pain, diagnosis
    +5 if all checks say "No conflicts"

    Compliance (40–90):
    Base 65
    +10 if pdpm_alignment.summary present
    +5 if pdpm_alignment.notes present
    -10 if safety_concerns exist
    -5 if follow_up missing
    -10 if any risk_flag severity = high

    Risk Level:
    High → any high
    Medium → ≥1 medium, no high
    Low → none or only low

    Missing data must NOT increase risk.
"""
