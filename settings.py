import os

from dotenv import load_dotenv

load_dotenv()

# --- AnkiConnect Settings ---
ANKICONNECT_URL = os.getenv("ANKICONNECT_URL", "http://localhost:8765")
ANKICONNECT_AUTH_TOKEN = os.getenv("ANKICONNECT_AUTH_TOKEN")
ANKICONNECT_API_VERSION = 6

# --- LLM Settings ---
# Available Models
MODEL_GPT3 = "gpt-3.5-turbo"
MODEL_DEEPSEEK_FREE = "deepseek/deepseek-r1:free"
MODEL_GEMINI_2_FLASH = "google/gemini-2.0-flash-001"
MODEL_GEMINI_2_5_PRO = "google/gemini-2.5-pro-preview"

# Default Model to Use
USE_MODEL = os.getenv("LLM_MODEL_TO_USE", MODEL_DEEPSEEK_FREE)

# OpenRouter Parameters (if using OpenRouter models)
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# --- Mailjet Settings ---
MAILJET_API_KEY = os.getenv("MAILJET_API_KEY")
MAILJET_SECRET_KEY = os.getenv("MAILJET_SECRET_KEY")
MAILJET_SENDER_EMAIL = os.getenv(
    "MAILJET_SENDER_EMAIL", "your_verified_sender@example.com"
)

RECIPIENT_EMAIL = "gustaf.gyllensporre@gmail.com"
