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