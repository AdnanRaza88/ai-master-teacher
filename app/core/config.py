import os

class Settings:
    APP_NAME: str = "AI Master Teacher"
    LLM_MODEL: str = "gemma-4"
    LLM_API_URL: str = os.getenv("LLM_API_URL", "http://localhost:8001/generate")
    AI_THINKING_DELAY: float = float(os.getenv("AI_THINKING_DELAY", 1.2))

settings = Settings()
