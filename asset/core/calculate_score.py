def to_number(value):
    """
    Safely convert score value to number.
    Assumes value is already numeric at runtime.
    """
    return float(value)


def calculate_documentation_quality(data):
    summary = data["summary"]

    summary_total = sum([
        to_number(summary["session_type"]["score"]),
        to_number(summary["presenting_concerns"]["score"]),
        to_number(summary["interventions_used"]["score"]),
        to_number(summary["response"]["score"]),
        to_number(summary["progress_toward_goals"]["score"]),
        to_number(summary["clinical_impression"]["score"]),
        to_number(summary["safety_concerns"]["score"]),
        to_number(summary["follow_up"]["score"]),
        to_number(summary["brief_notes"]["score"])
    ])

    pdpm_summary = to_number(data["pdpm_alignment"]["summary"]["score"])

    documentation_quality = (summary_total + pdpm_summary) * 10
    return round(documentation_quality, 2)


def calculate_consistency_score(data):
    checks = data["consistency_checks"]

    consistency_score = sum([
        to_number(checks["adl_conflicts"]["score"]),
        to_number(checks["behavior_conflicts"]["score"]),
        to_number(checks["therapy_conflicts"]["score"]),
        to_number(checks["pain_conflicts"]["score"]),
        to_number(checks["diagnosis_alignment"]["score"])
    ]) 

    consistency_score = consistency_score * 20

    return round(consistency_score, 2)


def calculate_compliance_score(data):
    risk_scores = []

    for risk in data["risk_flags"]:
        risk_total = sum([
            to_number(risk["category"]["score"]),
            to_number(risk["description"]["score"]),
            to_number(risk["why_it_matters"]["score"]),
            to_number(risk["evidence"]["score"]),
            to_number(risk["severity"]["score"])
        ])
        risk_scores.append((risk_total / 6) * 100)

    risk_score = sum(risk_scores) / len(risk_scores) if risk_scores else 100

    safety_pdpm_total = sum([
        to_number(data["summary"]["safety_concerns"]["score"]),
        to_number(data["summary"]["follow_up"]["score"]),
        to_number(data["pdpm_alignment"]["summary"]["score"]),
        to_number(data["pdpm_alignment"]["notes"]["score"])
    ])

    safety_pdpm_score = (safety_pdpm_total / 3) * 100

    compliance_score = (risk_score + safety_pdpm_score) / 2 
    return round(compliance_score, 2)


def calculate_overall_score(documentation_quality, consistency_score, compliance_score):
    overall_score = (
        4 * documentation_quality +
        3 * consistency_score +
        3 * compliance_score
    ) / 10

    return round(overall_score, 2)

def calculate_scores(data):
    documentation_quality = calculate_documentation_quality(data)
    consistency_score = calculate_consistency_score(data)
    compliance_score = calculate_compliance_score(data)
    overall_score = calculate_overall_score(
        documentation_quality,
        consistency_score,
        compliance_score
    )
    if overall_score < 40:
        risk_level = 'high'
    elif 40 <= overall_score < 75:
        risk_level = 'medium'
    elif overall_score >= 75:
        risk_level = 'low'

    result = {
        'scores': {
            "documentation_quality": documentation_quality,
            "consistency_score": consistency_score,
            "compliance_score": compliance_score,
            "risk_level": risk_level,
            "overall_score": overall_score
        }
    }
    return result



"""documentation_quality = calculate_documentation_quality(out_temp)
consistency_score = calculate_consistency_score(out_temp)
compliance_score = calculate_compliance_score(out_temp)
overall_score = calculate_overall_score(
    documentation_quality,
    consistency_score,
    compliance_score
)

print("Documentation Quality:", documentation_quality)
print("Consistency Score:", consistency_score)
print("Compliance Score:", compliance_score)
print("Overall Score:", overall_score)

score = {
    "documentation_quality": documentation_quality,
    "consistency_score": consistency_score,
    "compliance_score": compliance_score,
    "overall_score": overall_score
}
"""
