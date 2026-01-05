from asset.core.output_temp import out_temp
from langchain_core.prompts import PromptTemplate
from langchain.messages import SystemMessage, HumanMessage

def GenPrompt(report_data):

    
    sys_message = SystemMessage(
        content=(
            "You are a specialist Report Analyst. "
            "You analyze reports and focus on insights, trends, risks, and implications rather than document structure. "
            "You must write in clear, non-technical, executive-level language suitable for "
            "MDS Coordinators, Administrators, and Corporate teams. "
            "Do not hallucinate "
            "Do NOT include clinical terminology or implementation details. "
            "Follow the output structure STRICTLY and return ONLY valid JSON. "
            "And When calculate scores do not give absulut 0. cause report have insufficient data not dangares"
            "Do not include explanations, comments, or extra text, or do not need betify like ```json ```."
            f"Output structure: {out_temp}"
        )
    )
    print(out_temp)

    hum_message = HumanMessage(
        content=f"Report: {report_data}"
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