import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Read API key securely
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")

# Validate configuration early
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing. Please check your .env file.")