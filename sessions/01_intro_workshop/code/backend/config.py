# config.py
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# GitHub and Groq configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

config_openai = {
    "account": "abbe3864d6e415d5692f79c3964262e8",
    "gateway_id": "aiproxy",
    "provider": "openai",
    "model": "gpt-3.5-turbo",
    "endpoint": "chat/completions",
    "auth_token": OPENAI_API_KEY
}

config_groq = {
    "account": "abbe3864d6e415d5692f79c3964262e8",
    "gateway_id": "aiproxy",
    "provider": "groq",
    "model": "mixtral-8x7b-32768",
    "endpoint": "chat/completions",
    "auth_token": GROQ_API_KEY
}

print("Configuration loaded successfully.")