from docx import Document

def extract_docx(file_path):

    document = Document(file_path)
    fullText = []
    for para in document.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)





