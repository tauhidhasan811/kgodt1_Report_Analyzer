# from langchain_google_genai import ChatGoogleGenerativeAI
# #google gemini flash 2.5 model
# def GenModel(model_name):
#     model = ChatGoogleGenerativeAI(
#         model = model_name,
#         temperature=0.0
#     )
#     return model

from langchain_google_genai import ChatGoogleGenerativeAI

def GenModel(model_name, fixed_seed=42):
    generation_config = {
        "temperature":0,
        "top_p":1,
        "top_k":1
    }

    model = ChatGoogleGenerativeAI(
        model = model_name,
        temperature = 0,
        generation_config = generation_config

    )
    return model