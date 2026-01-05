import os
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

def ocr_image_with_gemini(image_path: str) -> str:
    image = Image.open(image_path)

    prompt = """
    Extract all readable text from this image.
    Preserve layout, headings, bullet points, and tables.
    Do not add explanations.
    """

    response = model.generate_content([prompt, image])
    return response.text.strip()