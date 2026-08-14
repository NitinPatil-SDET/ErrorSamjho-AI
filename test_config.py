from connection import (
    ENV_FILE,
    GROQ_API_KEY,
    GROQ_BASE_URL,
    GROQ_MODEL,
)


print("Environment file:", ENV_FILE)
print("Environment file exists:", ENV_FILE.exists())
print("API key loaded:", bool(GROQ_API_KEY))
print("API key starts correctly:", GROQ_API_KEY.startswith("gsk_"))
print("API key length:", len(GROQ_API_KEY))
print("Base URL:", GROQ_BASE_URL)
print("Model:", GROQ_MODEL)