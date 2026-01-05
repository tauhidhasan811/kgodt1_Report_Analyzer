def extract_txt(file_path):
    text = ''
    with open(file_path, 'r') as f:
        text = text+f.read()
    
    return text