from openai import OpenAI

#API key and OPENAI model loaded from config.py
from app.config import OPENAI_API_KEY, OPENAI_MODEL

# Create a client for communicating with the OpenAI API
client = OpenAI(
    api_key=OPENAI_API_KEY,
)

#defines a reusable function
def ask_llm(question: str) -> str:
    """
    Sends a question to the LLM and returns the response.
    """
    
    #sends a request to the OpenAI API. The user's question becomes the input sent to the model.
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=question,
    )

    #output_text extracts just the generated text for us
    return response.output_text