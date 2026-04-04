"""
Application configuration loaded from environment variables.
Falls back to demo/mock mode when OPENAI_API_KEY is not set.
"""
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

# LLM
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Demo mode activates when no real API key is present
USE_MOCK: bool = not bool(OPENAI_API_KEY) or OPENAI_API_KEY.startswith("your-")

# Search
ARXIV_MAX_RESULTS: int = int(os.getenv("ARXIV_MAX_RESULTS", "5"))
SEMANTIC_SCHOLAR_MAX_RESULTS: int = int(os.getenv("SEMANTIC_SCHOLAR_MAX_RESULTS", "5"))

# Server
APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT: int = int(os.getenv("APP_PORT", "8000"))

# Pipeline
MAX_ITERATIONS: int = int(os.getenv("MAX_ITERATIONS", "1"))
