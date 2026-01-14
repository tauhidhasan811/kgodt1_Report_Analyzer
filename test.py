"""from dotenv import load_dotenv
from asset.service.gen_model import GenModel
from asset.core.prompt import GenPrompt
from asset.service.document_extractor import extract_document

load_dotenv()

try:
    doc_text = extract_document("test_files/test 1.png")
    print("---Extracted Text start ----")
    print(doc_text)
    print("---Extracted Text end ----")
    model = GenModel(model_name='gemini-2.5-flash')
    
    prompt = GenPrompt(report_data=doc_text)
    response = model.invoke(prompt).content
    print(response)

except Exception as ex:
    print(str(ex))"""


"""from asset.service.document_extractor.docx_utils import extract_docx

path = 'The Cow.doc'

print(extract_docx(path))"""

"""from asset.service.document_extractor.text_utils import extract_txt


print(extract_txt('The Cow.txt'))"""


from asset.core.extract_values import extract_values
from asset.core.calculate_score import calculate_scores

data ={"summary": {"session_type": {"value": "Work Progress Update", "score": 0.8}, "presenting_concerns": {"value": "Improving report analysis consistency was a key focus.", "score": 0.8}, "interventions_used": {"value": "Model logic and prompts were enhanced, the model was successfully deployed to Render, comprehensive testing was performed, and team collaboration was maintained.", "score": 1.8}, "response": {"value": "The model was successfully deployed and tested, verifying accuracy, stability, and performance.", "score": 0.9}, "progress_toward_goals": {"value": "Significant progress was made in improving report analysis consistency and achieving successful model deployment.", "score": 0.9}, "clinical_impression": {"value": "Positive progress on key development and deployment milestones.", "score": 0.7}, "safety_concerns": {"value": "No safety concerns are indicated in this technical work report.", "score": 0.1}, "follow_up": {"value": "No specific follow-up actions are detailed in this report.", "score": 0.1}, "brief_notes": {"value": "Model successfully deployed and tested, with improved consistency.", "score": 0.4}}, "risk_flags": [{"category": {"value": "Operational Monitoring", "score": 0.8}, "description": {"value": "Ongoing monitoring is essential to ensure the model maintains its accuracy, stability, and performance in a live environment.", "score": 0.8}, "why_it_matters": {"value": "Sustained performance is critical for reliable report analysis and user confidence.", "score": 0.8}, "evidence": {"value": "The model was tested, but real-world usage can introduce new variables requiring continuous oversight.", "score": 1.5}, "severity": {"value": "low", "score": 0.3}}], "pdpm_alignment": {"summary": {"value": "This report pertains to technical model development and deployment, not patient care or reimbursement, therefore PDPM alignment is not applicable.", "score": 0.1}, "notes": {"value": "The content of this work report focuses on software development, deployment, and testing activities, which fall outside the scope of the Patient-Driven Payment Model (PDPM).", "score": 0.1}}, "consistency_checks": {"adl_conflicts": {"value": "This report is technical and does not contain information related to Activities of Daily Living (ADLs).", "score": 0.1}, "behavior_conflicts": {"value": "This report is technical and does not contain information related to resident behaviors.", "score": 0.1}, "therapy_conflicts": {"value": "This report is technical and does not contain information related to therapy services.", "score": 0.1}, "pain_conflicts": {"value": "This report is technical and does not contain information related to pain management.", "score": 0.1}, "diagnosis_alignment": {"value": "This report is technical and does not contain information related to resident diagnoses.", "score": 0.1}}}

result = {}
result_text = extract_values(data)
result_scores = calculate_scores(data)
result.update(result_text)
result.update(result_scores)
message = result
print(message)