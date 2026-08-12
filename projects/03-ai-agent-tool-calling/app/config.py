# This centralizes all application configuration and validates it during startup.

# reads environment variables.
import os

# creates a clean configuration object
from dataclasses import dataclass

# loads values from the local .env file.
from dotenv import load_dotenv

# Makes values from .env file available to Python
load_dotenv()


# Defines the settings your application needs
@dataclass(
    frozen=True
)  # values cannot be changed accidentally after the object is created.
class Settings:
    openai_api_key: str
    openai_model: str
    agent_max_iterations: int
    log_level: str


# Reads, validates, and returns all configuration values
def load_settings() -> Settings:

    # API key
    api_key = os.getenv("OPENAI_API_KEY", "").strip()

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is missing. " "Create a .env file based on .env.example."
        )

    # Iteration limit
    max_iterations_text = os.getenv("AGENT_MAX_ITERATIONS", "5")

    try:
        max_iterations = int(max_iterations_text)
    except ValueError as exc:
        raise ValueError("AGENT_MAX_ITERATIONS must be an integer.") from exc

    if max_iterations < 1:
        raise ValueError("AGENT_MAX_ITERATIONS must be greater than zero.")

    return Settings(
        openai_api_key=api_key,
        openai_model=os.getenv(
            "OPENAI_MODEL",
            "gpt-5.4-mini",
        ),
        agent_max_iterations=max_iterations,
        log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
    )


# Global settings instance
settings = load_settings()
