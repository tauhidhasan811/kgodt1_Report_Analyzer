from langchain_openai import ChatOpenAI

def LoadGPT(model_name='gpt-4.1-2025-04-14'):
    model = ChatOpenAI(
        model=model_name,
        temperature=0.0
    )
    return model