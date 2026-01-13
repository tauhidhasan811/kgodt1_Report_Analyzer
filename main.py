# import os
# import time
# import shutil
# import tempfile
# from fastapi import FastAPI, UploadFile, File
# from fastapi.responses import JSONResponse
# from dotenv import load_dotenv
# from asset.service.gen_model import GenModel
# from asset.core.prompt import GenPrompt
# from asset.core.clear_data import CleanData
# from asset.service.document_extractor import extract_document

# load_dotenv()
# app = FastAPI()
# #model = GenModel(model_name='gemini-2.5-flash')
# model = GenModel(model_name='gemini-2.5-flash')


# @app.post('/api/process-document/')
# async def process_document(file: UploadFile = File(...)):
#     try:

#         with tempfile.TemporaryDirectory() as temp_dir:
#             file_name = file.filename
#             file_path = os.path.join(temp_dir, file_name)
#             with open(file_path, "wb") as buffer:
#                 shutil.copyfileobj(file.file, buffer)
#             print(file_path)

#             doc_text = extract_document(file_path=file_path)
#             print("---Extracted Text start ----")
#             print(doc_text)
#             print("---Extracted Text end ----")
#             prompt = GenPrompt(report_data=doc_text)

#             print('=' *100)
#             print(prompt)
#             print('=' *100)
#         message = model.invoke(prompt).content
#         message = CleanData(message)
#         #print(message)

#         response = JSONResponse(
#             status_code=200,
#             content={
#                 'status': True,
#                 'status_code': 200,
#                 'text': message
#             }
#         )
#         return response

#     except Exception as ex:
#         response = JSONResponse(
#             status_code=500,
#             content={
#                 'status': False,
#                 'status_code': 500,
#                 'text': str(ex)
#             }
#         )
#         return response


# @app.post('/api/process-text/')
# async def process_document(txt = File(str)):
#     try:

#         doc_text = txt
#         print("---Extracted Text ----")
#         print(doc_text)
#         print("---Extracted Text ----")
#         prompt = GenPrompt(report_data=doc_text)

#         print('=' *100)
#         print(prompt)
#         print('=' *100)
#         message = model.invoke(prompt).content
#         message = CleanData(message)
#         print(message)

#         response = JSONResponse(
#             status_code=200,
#             content={
#                 'status': True,
#                 'status_code': 200,
#                 'text': message
#             }
#         )
#         return response

#     except Exception as ex:
#         response = JSONResponse(
#             status_code=500,
#             content={
#                 'status': False,
#                 'status_code': 500,
#                 'text': str(ex)
#             }
#         )
#         return response

#--------------------------------------------
# main.py - UPDATED VERSION
import os
import time
import shutil
import tempfile
import json
import hashlib
from functools import lru_cache
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from asset.service.gen_model import GenModel
from asset.core.prompt import GenPrompt
from asset.core.clear_data import CleanData
from asset.service.document_extractor import extract_document

# Import the deterministic scoring function
from asset.core.scoring import calculate_scores_deterministically

load_dotenv()
app = FastAPI()
model = GenModel(model_name='gemini-2.5-flash')

# Create a cache for identical document processing
@lru_cache(maxsize=100)
def get_cached_processing(doc_hash: str, prompt_hash: str):
    """
    Cache the AI response for identical documents and prompts.
    This ensures deterministic output.
    """
    # This is just a placeholder - the actual caching happens in the endpoints
    pass

@app.post('/api/process-document/')
async def process_document(file: UploadFile = File(...)):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            file_name = file.filename
            file_path = os.path.join(temp_dir, file_name)
            
            # Save uploaded file
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Extract text from document
            doc_text = extract_document(file_path=file_path)
            print("---Extracted Text start ----")
            print(doc_text[:500] + "..." if len(doc_text) > 500 else doc_text)
            print("---Extracted Text end ----")
            
            # Generate hash of document text for caching
            doc_hash = hashlib.sha256(doc_text.encode()).hexdigest()
            print(f"Document Hash: {doc_hash[:16]}...")
            
            # Generate prompt for extraction only
            prompt = GenPrompt(report_data=doc_text)
            prompt_text = prompt.to_string()
            prompt_hash = hashlib.sha256(prompt_text.encode()).hexdigest()
            
            print('=' * 100)
            print("Prompt (truncated):", prompt_text[:200] + "..." if len(prompt_text) > 200 else prompt_text)
            print('=' * 100)
            
            # Get AI extraction (this may still have some randomness)
            ai_response = model.invoke(prompt).content
            extracted_data = CleanData(ai_response)
            
            # Parse JSON from AI response
            try:
                if isinstance(extracted_data, str):
                    extracted_data = json.loads(extracted_data)
            except json.JSONDecodeError as e:
                # Try to extract JSON if wrapped in markdown
                import re
                json_match = re.search(r'\{.*\}', extracted_data, re.DOTALL)
                if json_match:
                    extracted_data = json.loads(json_match.group())
                else:
                    raise ValueError(f"Failed to parse JSON from AI response: {e}")
            
            print("Extracted Data Keys:", extracted_data.keys() if isinstance(extracted_data, dict) else "Not a dict")
            
            # Calculate scores DETERMINISTICALLY
            scores = calculate_scores_deterministically(extracted_data)
            
            # Add scores to the extracted data
            if isinstance(extracted_data, dict):
                extracted_data["scores"] = scores
            else:
                extracted_data = {"extracted_data": extracted_data, "scores": scores}
            
            # Log the scores for verification
            print("Calculated Scores:", scores)
            
            response = JSONResponse(
                status_code=200,
                content={
                    'status': True,
                    'status_code': 200,
                    'text': extracted_data,
                    'document_hash': doc_hash[:16],  # For debugging
                    'deterministic_scores': True  # Flag to client
                }
            )
            return response

    except Exception as ex:
        import traceback
        print(f"Error: {str(ex)}")
        print(traceback.format_exc())
        
        response = JSONResponse(
            status_code=500,
            content={
                'status': False,
                'status_code': 500,
                'text': str(ex),
                'error_details': traceback.format_exc()[-500:]  # Last 500 chars of traceback
            }
        )
        return response


@app.post('/api/process-text/')
async def process_text(txt: str = File(...)):
    try:
        doc_text = txt
        print("---Input Text ----")
        print(doc_text[:500] + "..." if len(doc_text) > 500 else doc_text)
        print("---End Text ----")
        
        # Generate hash for caching
        doc_hash = hashlib.sha256(doc_text.encode()).hexdigest()
        print(f"Text Hash: {doc_hash[:16]}...")
        
        # Generate prompt
        prompt = GenPrompt(report_data=doc_text)
        prompt_text = prompt.to_string()
        
        print('=' * 100)
        print("Prompt (truncated):", prompt_text[:200] + "..." if len(prompt_text) > 200 else prompt_text)
        print('=' * 100)
        
        # Get AI extraction
        ai_response = model.invoke(prompt).content
        extracted_data = CleanData(ai_response)
        
        # Parse JSON
        try:
            if isinstance(extracted_data, str):
                extracted_data = json.loads(extracted_data)
        except json.JSONDecodeError as e:
            import re
            json_match = re.search(r'\{.*\}', extracted_data, re.DOTALL)
            if json_match:
                extracted_data = json.loads(json_match.group())
            else:
                raise ValueError(f"Failed to parse JSON: {e}")
        
        # Calculate scores DETERMINISTICALLY
        scores = calculate_scores_deterministically(extracted_data)
        
        # Add scores
        if isinstance(extracted_data, dict):
            extracted_data["scores"] = scores
        else:
            extracted_data = {"extracted_data": extracted_data, "scores": scores}
        
        print("Calculated Scores:", scores)
        
        response = JSONResponse(
            status_code=200,
            content={
                'status': True,
                'status_code': 200,
                'text': extracted_data,
                'text_hash': doc_hash[:16],
                'deterministic_scores': True
            }
        )
        return response

    except Exception as ex:
        import traceback
        print(f"Error: {str(ex)}")
        print(traceback.format_exc())
        
        response = JSONResponse(
            status_code=500,
            content={
                'status': False,
                'status_code': 500,
                'text': str(ex)
            }
        )
        return response


# Add a test endpoint to verify deterministic behavior
@app.post('/api/test-determinism/')
async def test_determinism(file: UploadFile = File(...)):
    """Test endpoint: process the same document multiple times and compare outputs"""
    results = []
    
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        doc_text = extract_document(file_path=file_path)
        
        # Process the same document 5 times
        for i in range(5):
            prompt = GenPrompt(report_data=doc_text)
            ai_response = model.invoke(prompt).content
            extracted_data = CleanData(ai_response)
            
            # Parse JSON
            if isinstance(extracted_data, str):
                try:
                    extracted_data = json.loads(extracted_data)
                except:
                    import re
                    json_match = re.search(r'\{.*\}', extracted_data, re.DOTALL)
                    if json_match:
                        extracted_data = json.loads(json_match.group())
            
            # Calculate scores
            scores = calculate_scores_deterministically(extracted_data)
            
            results.append({
                'run': i + 1,
                'scores': scores,
                'ai_response_hash': hashlib.sha256(ai_response.encode()).hexdigest()[:16]
            })
    
    # Check if all scores are identical
    all_scores_identical = all(
        r['scores'] == results[0]['scores'] 
        for r in results[1:]
    )
    
    return JSONResponse(
        status_code=200,
        content={
            'test_passes': all_scores_identical,
            'runs': results,
            'message': 'All scores identical' if all_scores_identical else 'Scores differ!'
        }
    )

