from langchain_google_genai import ChatGoogleGenerativeAI
#google gemini flash 2.5 model
def GenModel(model_name):
    model = ChatGoogleGenerativeAI(
        model = model_name,
        temperature=0.0
    )
    return model