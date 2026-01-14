def extract_values(data):
    return {
        "summary": {
            "session_type": data["summary"]["session_type"]["value"],
            "presenting_concerns": data["summary"]["presenting_concerns"]["value"],
            "interventions_used": data["summary"]["interventions_used"]["value"],
            "response": data["summary"]["response"]["value"],
            "progress_toward_goals": data["summary"]["progress_toward_goals"]["value"],
            "clinical_impression": data["summary"]["clinical_impression"]["value"],
            "safety_concerns": data["summary"]["safety_concerns"]["value"],
            "follow_up": data["summary"]["follow_up"]["value"],
            "brief_notes": data["summary"]["brief_notes"]["value"]
        },

        "risk_flags": [
            {
                "category": risk["category"]["value"],
                "description": risk["description"]["value"],
                "why_it_matters": risk["why_it_matters"]["value"],
                "evidence": risk["evidence"]["value"],
                "severity": risk["severity"]["value"]
            }
            for risk in data["risk_flags"]
        ],

        "pdpm_alignment": {
            "summary": data["pdpm_alignment"]["summary"]["value"],
            "notes": data["pdpm_alignment"]["notes"]["value"]
        },

        "consistency_checks": {
            "adl_conflicts": data["consistency_checks"]["adl_conflicts"]["value"],
            "behavior_conflicts": data["consistency_checks"]["behavior_conflicts"]["value"],
            "therapy_conflicts": data["consistency_checks"]["therapy_conflicts"]["value"],
            "pain_conflicts": data["consistency_checks"]["pain_conflicts"]["value"],
            "diagnosis_alignment": data["consistency_checks"]["diagnosis_alignment"]["value"]
        }
    }
