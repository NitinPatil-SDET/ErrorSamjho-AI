import os
from pathlib import Path

import httpx
from dotenv import load_dotenv
from openai import OpenAI


# Find the .env file from the current Python file location
BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

# Override any old Windows environment variable
load_dotenv(dotenv_path=ENV_FILE, override=True)


GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()

GROQ_BASE_URL = os.getenv(
    "GROQ_BASE_URL",
    "https://api.groq.com/openai/v1",
).strip()

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile",
).strip()


def validate_configuration():
    if not ENV_FILE.exists():
        raise ValueError(
            f".env file was not found at: {ENV_FILE}"
        )

    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY is missing or empty in the .env file."
        )

    if not GROQ_API_KEY.startswith("gsk_"):
        raise ValueError(
            "GROQ_API_KEY does not look valid. "
            "A Groq API key should normally start with 'gsk_'."
        )


def create_groq_client():
    validate_configuration()

    return OpenAI(
        api_key=GROQ_API_KEY,
        base_url=GROQ_BASE_URL,
        http_client=httpx.Client(
            verify=False,
            timeout=30.0,
        ),
        max_retries=2,
    )