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

from asset.service.document_extractor.text_utils import extract_txt

print(extract_txt('The Cow.txt'))