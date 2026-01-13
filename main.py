import os
import time
import shutil
import tempfile
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from asset.service.gen_model import GenModel
from asset.core.prompt import GenPrompt
from asset.core.clear_data import CleanData
from asset.service.document_extractor import extract_document
from asset.core.calculate_score import calculate_scores
from asset.core.extract_values import extract_values

load_dotenv()
app = FastAPI()
#model = GenModel(model_name='gemini-2.5-flash')
model = GenModel(model_name='gemini-2.5-flash')

print('x' * 100)
print('Api key is : ', os.environ.get('GOOGLE_API_KEY'))
print('x' * 100)

@app.post('/api/process-document/')
async def process_document(file: UploadFile = File(...)):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            file_name = file.filename
            file_path = os.path.join(temp_dir, file_name)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            print(file_path)

            doc_text = extract_document(file_path=file_path)
            print("---Extracted Text start ----")
            #print(doc_text)
            print("---Extracted Text end ----")
            prompt = GenPrompt(report_data=doc_text)

            print('=' *100)
            #print(prompt)
            print('=' *100)
        message = model.invoke(prompt).content
        message = CleanData(message)
        #print(message)
        result = {}
        result_text = extract_values(message)
        result_scores = calculate_scores(message)
        result.update(result_text)
        result.update(result_scores)
        message = result

        response = JSONResponse(
            status_code=200,
            content={
                'status': True,
                'status_code': 200,
                'text': message
            }
        )
        return response

    except Exception as ex:
        response = JSONResponse(
            status_code=500,
            content={
                'status': False,
                'status_code': 500,
                'text': str(ex)
            }
        )
        return response


@app.post('/api/process-text/')
async def process_document(txt = File(str)):
    try:

        doc_text = txt
        print("---Extracted Text ----")
        print(doc_text)
        print("---Extracted Text ----")
        prompt = GenPrompt(report_data=doc_text)

        print('=' *100)
        print(prompt)
        print('=' *100)
        message = model.invoke(prompt).content
        message = CleanData(message)
        print(message)

        response = JSONResponse(
            status_code=200,
            content={
                'status': True,
                'status_code': 200,
                'text': message
            }
        )
        return response

    except Exception as ex:
        response = JSONResponse(
            status_code=500,
            content={
                'status': False,
                'status_code': 500,
                'text': str(ex)
            }
        )
        return response


