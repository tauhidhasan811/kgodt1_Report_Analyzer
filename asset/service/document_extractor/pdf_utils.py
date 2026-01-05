import fitz
import os

def extract_pdf_text_and_images(pdf_path: str):
    doc = fitz.open(pdf_path)

    extracted_text = ""
    #image_paths = []

    for page_index, page in enumerate(doc):
        text = page.get_text().strip()
        if text:
            extracted_text += f"\n--- Page {page_index + 1} ---\n{text}"

        #pix = page.get_pixmap(dpi=300)
        #image_path = f"temp_page_{page_index}.png"
        #pix.save(image_path)
        #image_paths.append(image_path)

    #return extracted_text, image_paths
    return extracted_text
