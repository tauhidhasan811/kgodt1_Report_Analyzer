out_temp = {
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
            "documentation_quality": 0,
            "consistency_score": 0,
            "compliance_score": 0,
            "risk_level": "high | medium | low"
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
