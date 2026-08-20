import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

# Load .env only during local development
if ENV_FILE.exists():
    load_dotenv(dotenv_path=ENV_FILE, override=True)


def _get_int_env(name, default):
    value = os.getenv(name, str(default)).strip()
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()

GROQ_BASE_URL = os.getenv(
    "GROQ_BASE_URL",
    "https://api.groq.com/openai/v1",
).strip()

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-20b",
).strip()

MAX_SESSION_REQUESTS = _get_int_env("MAX_SESSION_REQUESTS", 8)
API_REQUEST_COOLDOWN_SECONDS = _get_int_env("API_REQUEST_COOLDOWN_SECONDS", 10)
DUPLICATE_REQUEST_WINDOW_SECONDS = _get_int_env("DUPLICATE_REQUEST_WINDOW_SECONDS", 30)
MAX_ERROR_LOG_LENGTH = _get_int_env("MAX_ERROR_LOG_LENGTH", 20000)
MIN_ERROR_LOG_LENGTH = _get_int_env("MIN_ERROR_LOG_LENGTH", 10)


def validate_configuration():
    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY is missing. Add it to the local .env file "
            "or Streamlit Cloud secrets."
        )

    if not GROQ_API_KEY.startswith("gsk_"):
        raise ValueError(
            "GROQ_API_KEY is invalid. A Groq API key should "
            "normally start with 'gsk_'."
        )


def create_groq_client():
    validate_configuration()

    return OpenAI(
        api_key=GROQ_API_KEY,
        base_url=GROQ_BASE_URL,
        timeout=30.0,
        max_retries=2,
    )