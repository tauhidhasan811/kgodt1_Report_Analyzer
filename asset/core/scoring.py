import re
def calculate_scores_deterministically(extracted_data):
    #calculate scores based on extracted data using fixed rules

    doc_quality = 60 #base for documentation quality
    consistency = 75 # base for consistency
    compliance = 65 # this is base for compliance

    # Documentation quality summary
    summary = extracted_data.get('summary',{})
    risk_flags = extracted_data.get('risk_flags',{})
    pdpm_alignment = extracted_data.get('pdpm_alignment',{})
    consistency_checks = extracted_data.get('consistency_checks',{})

    #documentation quality calculation 45- 90 range
    #these fields contribute to +5 if present and valid
    present_fields = [
        'session_type', 'presenting_concerns', 'interventions_used',
        'response', 'progress_toward_goals', 'follow_up'
    ]

    #counting how many fields are presnet and how many are not

    present_count = 0
    not_documented_count = 0

    for field in present_fields:
        field_value = summary.get(field,'')
        if isinstance(field_value, str):
            field_value = field_value.strip()
            if field_value and field_value.lower()!= 'not documented':
                present_count +=1
            
            elif field_value.lower() == 'not documented':
                not_documented_count +=1 
    
    #applying the rules
    doc_quality += (present_count * 5)
     # -5 if 2+ summary fields = "Not documented"
    if not_documented_count >= 2:
        doc_quality -= 5
    
    # -5 if brief_notes is vague
    brief_notes = summary.get('brief_notes', '')
    if isinstance(brief_notes, str):
        brief_notes_lower = brief_notes.lower()
        vague_indicators = ['vague', 'unclear', 'not specified', 'none', 'na', 'n/a', 'tbd']
        if any(indicator in brief_notes_lower for indicator in vague_indicators):
            doc_quality -= 5
    
    # -10 if summary text largely duplicated (simple check)
    # Collect all summary text
    summary_texts = []
    for key, value in summary.items():
        if isinstance(value, str) and value.strip():
            summary_texts.append(value.strip())
    
    if len(summary_texts) >= 2:
        # Simple duplication check: if any text appears multiple times
        text_counts = {}
        for text in summary_texts:
            # Take first 50 chars as a fingerprint
            fingerprint = text[:50].lower()
            text_counts[fingerprint] = text_counts.get(fingerprint, 0) + 1
        
        # If any fingerprint appears more than once, consider it duplicated
        if any(count > 1 for count in text_counts.values()):
            doc_quality -= 10
    
    # Clamp to range 45-90
    doc_quality = max(45, min(90, doc_quality))
    
    # --- Consistency Score Calculation (50-85) ---
    conflict_fields = [
        'adl_conflicts', 'behavior_conflicts', 'therapy_conflicts',
        'pain_conflicts', 'diagnosis_alignment'
    ]
    
    # Count conflicts (anything not "No" or empty)
    conflict_count = 0
    all_no_conflicts = True
    
    for field in conflict_fields:
        field_value = consistency_checks.get(field, '')
        if isinstance(field_value, str):
            field_value_lower = field_value.strip().lower()
            # Check if it indicates a conflict
            if field_value_lower and field_value_lower not in ['no', 'no conflicts', 'none', '']:
                conflict_count += 1
                all_no_conflicts = False
    
    consistency -= (conflict_count * 10)
    
    # +5 if all checks say "No conflicts"
    if all_no_conflicts:
        consistency += 5
    
    # Clamp to range 50-85
    consistency = max(50, min(85, consistency))
    
    # --- Compliance Score Calculation (40-90) ---
    # +10 if pdpm_alignment.summary present
    if pdpm_alignment.get('summary', ''):
        compliance += 10
    
    # +5 if pdpm_alignment.notes present
    if pdpm_alignment.get('notes', ''):
        compliance += 5
    
    # -10 if safety_concerns exist
    safety_concerns = summary.get('safety_concerns', '')
    if safety_concerns and isinstance(safety_concerns, str) and safety_concerns.strip():
        compliance -= 10
    
    # -5 if follow_up missing
    follow_up = summary.get('follow_up', '')
    if not follow_up or (isinstance(follow_up, str) and not follow_up.strip()):
        compliance -= 5
    
    # -10 if any risk_flag severity = high
    high_risk_exists = False
    for flag in risk_flags:
        if isinstance(flag, dict):
            severity = flag.get('severity', '').lower()
            if severity == 'high':
                high_risk_exists = True
                break
    
    if high_risk_exists:
        compliance -= 10
    
    # Clamp to range 40-90
    compliance = max(40, min(90, compliance))
    
    # --- Risk Level Calculation ---
    risk_level = 'low'  # Default
    
    # Collect all severities
    severities = []
    for flag in risk_flags:
        if isinstance(flag, dict):
            severity = flag.get('severity', '').lower()
            if severity in ['high', 'medium', 'low']:
                severities.append(severity)
    
    if 'high' in severities:
        risk_level = 'high'
    elif 'medium' in severities:
        risk_level = 'medium'
    # else remains 'low'
    
    # Round scores to integers
    return {
        'documentation_quality': int(round(doc_quality)),
        'consistency_score': int(round(consistency)),
        'compliance_score': int(round(compliance)),
        'risk_level': risk_level
    }
    
