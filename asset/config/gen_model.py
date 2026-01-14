from langchain_google_genai import ChatGoogleGenerativeAI
#google gemini flash 2.5 model
def GenModel(model_name):
    model = ChatGoogleGenerativeAI(
        model = model_name,
        temperature=0.0,
        top_p=0.1,      # Use low top_p for determinism
        top_k=1
    )
    return model