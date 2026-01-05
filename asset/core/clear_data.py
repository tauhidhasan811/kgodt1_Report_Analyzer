import re

def CleanData(text):
    cleaned = text.replace("\\", "")

    cleaned = re.sub(r"`{1,3}", "", cleaned)

    #removing code language keywords
    cleaned = re.sub(r'\b(json|bash|python)\b', '', cleaned, flags=re.IGNORECASE)

    # Step 4: Remove newlines and extra spaces
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()

    print(cleaned)
    return cleaned