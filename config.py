# config.py
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).with_name(".env"))

class Settings:
    NOSIBLE_API_KEY = os.getenv("NOSIBLE_API_KEY", "")

    SCALEKIT_ENVIRONMENT_URL = os.getenv("SCALEKIT_ENVIRONMENT_URL", "")
    SCALEKIT_CLIENT_ID = os.getenv("SCALEKIT_CLIENT_ID", "")
    SCALEKIT_CLIENT_SECRET = os.getenv("SCALEKIT_CLIENT_SECRET", "")

    SCALEKIT_AUTHORIZATION_SERVERS = os.getenv("SCALEKIT_AUTHORIZATION_SERVERS", "")
    SCALEKIT_RESOURCE_NAME = os.getenv("SCALEKIT_RESOURCE_NAME", "")
    SCALEKIT_RESOURCE_DOCS_URL = os.getenv("SCALEKIT_RESOURCE_DOCS_URL", "")

    PORT = int(os.getenv("PORT", "8000"))
    ALLOW_DEV_NOAUTH = os.getenv("ALLOW_DEV_NOAUTH", "0") == "1"

settings = Settings()
