# from asset.core.output_temp import out_temp, score_rules
# from langchain_core.prompts import PromptTemplate
# from langchain.messages import SystemMessage, HumanMessage

# def GenPrompt(report_data):

    
#     sys_message = SystemMessage(
#         content=(
#             "You are a specialist Report Analyst. "
#             "You analyze reports and focus on insights, trends, risks, and implications rather than document structure. "
#             "You must write in clear, non-technical, executive-level language suitable for "
#             "MDS Coordinators, Administrators, and Corporate teams. "
#             "Do not hallucinate "
#             "Do NOT include clinical terminology or implementation details. "
#             "Follow the output structure STRICTLY and return ONLY valid JSON. "
#             "And When calculate scores do not give absulut 0. cause report have insufficient data not dangares"
#             f"And try to follow those rule :{score_rules}"
#             "Do not include explanations, comments, or extra text, or do not need betify like ```json ```."
#             f"Output structure: {out_temp}"
#         )
#     )
#     print(out_temp)

#     hum_message = HumanMessage(
#         content=f"Report Data: {report_data}"
#     )

#     tempt = PromptTemplate(
#         template="{sys_message}\n\n{hum_message}",
#         input_variables=['sys_message', 'hum_message']
#     )

#     prompt = tempt.invoke(
#         {
#             'sys_message': sys_message.content,
#             'hum_message': hum_message.content
#         }
#     )
#     return prompt

#---------------------
# asset/core/prompt.py
from asset.core.output_temp_without_scores import out_temp_without_scores  # Use version without scores
from langchain_core.prompts import PromptTemplate
from langchain.messages import SystemMessage, HumanMessage

def GenPrompt(report_data):
    
    sys_message = SystemMessage(
        content=(
            "You are a JSON data extractor. Your ONLY task is to extract structured data from the report.\n\n"
            "## CRITICAL RULES:\n"
            "1. Output ONLY valid JSON. No markdown, no explanations, no other text.\n"
            "2. If a field is not EXPLICITLY mentioned in the report, leave it as EMPTY STRING (\"\") or EMPTY ARRAY ([]).\n"
            "3. DO NOT INFER, INTERPRET, or ADD information not in the report.\n"
            "4. For 'consistency_checks': Output ONLY 'Yes' or 'No'. If not mentioned, use 'No'.\n"
            "5. For 'risk_flags': Only create a flag if there is EXPLICIT RISK MENTIONED. If no risks mentioned, output [] (empty array).\n"
            "6. For 'brief_notes': Only fill if there are notes about risk escalation. Otherwise empty string.\n"
            "7. Be CONSISTENT: Same report text → Same JSON output.\n\n"
            "## OUTPUT FORMAT (JSON):\n"
            f"{out_temp_without_scores}\n\n"
            "## REPORT TEXT:\n"
            "{report_data}\n\n"
            "## EXTRACTED JSON:"
        )
    )
    
    hum_message = HumanMessage(
        content=f"Report Data: {report_data}"
    )
    
    tempt = PromptTemplate(
        template="{sys_message}\n\n{hum_message}",
        input_variables=['sys_message', 'hum_message']
    )
    
    prompt = tempt.invoke(
        {
            'sys_message': sys_message.content,
            'hum_message': hum_message.content
        }
    )
    return prompt