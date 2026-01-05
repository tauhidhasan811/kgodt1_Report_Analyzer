import os
from .gemini_vision import ocr_image_with_gemini
from .pdf_utils import extract_pdf_text_and_images
from .docx_utils import extract_docx
from .text_utils import extract_txt


def extract_document(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()

    if ext in [".png", ".jpg", ".jpeg"]:
        return ocr_image_with_gemini(file_path)

    elif ext == ".pdf":
        #text, _ = extract_pdf_text_and_images(file_path)
        text= extract_pdf_text_and_images(file_path)

    elif ext == ".txt":
        text = extract_txt(file_path=file_path)

    elif ext == ".docx":
        text = extract_docx(file_path=file_path)

    else:
        text = f"Unsupported file type: {ext}"

    return text
