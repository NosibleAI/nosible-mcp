import os
from dotenv import load_dotenv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env", override=True)

class Settings:
    # ScaleKit Configuration
    SCALEKIT_ENVIRONMENT_URL: str = os.environ.get("SCALEKIT_ENVIRONMENT_URL", "")
    SCALEKIT_CLIENT_ID: str = os.environ.get("SCALEKIT_CLIENT_ID", "")
    SCALEKIT_CLIENT_SECRET: str = os.environ.get("SCALEKIT_CLIENT_SECRET", "")
    SCALEKIT_RESOURCE_IDENTIFIER: str = os.environ.get("SCALEKIT_RESOURCE_IDENTIFIER", "")
    SCALEKIT_RESOURCE_METADATA_URL: str = os.environ.get("SCALEKIT_RESOURCE_METADATA_URL", "")
    SCALEKIT_AUTHORIZATION_SERVERS: str = os.environ.get("SCALEKIT_AUTHORIZATION_SERVERS", "")
    SCALEKIT_AUDIENCE_NAME: str = os.environ.get("SCALEKIT_AUDIENCE_NAME", "")
    SCALEKIT_RESOURCE_NAME: str = os.environ.get("SCALEKIT_RESOURCE_NAME", "")
    SCALEKIT_RESOURCE_DOCS_URL: str = os.environ.get("SCALEKIT_RESOURCE_DOCS_URL", "")
    CLIENT_ID: str = os.environ.get("CLIENT_ID", "")
    CLIENT_SECRET: str = os.environ.get("CLIENT_SECRET", "")

    # NOSIBLE API Key
    NOSIBLE_API_KEY: str = os.environ.get("NOSIBLE_API_KEY", "")

    # Server Port
    PORT: int = int(os.environ.get("PORT", 10000))

    def __post_init__(self):
        if not self.SCALEKIT_RESOURCE_IDENTIFIER:
            raise ValueError("SCALEKIT_RESOURCE_IDENTIFIER environment variable not set")
        if not self.SCALEKIT_CLIENT_ID:
            raise ValueError("SCALEKIT_CLIENT_ID environment variable not set")
        if not self.SCALEKIT_CLIENT_SECRET:
            raise ValueError("SCALEKIT_CLIENT_SECRET environment variable not set")
        if not self.SCALEKIT_RESOURCE_DOCS_URL:
            raise ValueError("SCALEKIT_RESOURCE_DOCS_URL environment variable not set")
        if not self.SCALEKIT_ENVIRONMENT_URL:
            raise ValueError("SCALEKIT_ENVIRONMENT_URL environment variable not set")
        if not self.NOSIBLE_API_KEY:
            raise ValueError("NOSIBLE_API_KEY environment variable not set")
        if not self.SCALEKIT_RESOURCE_METADATA_URL:
            raise ValueError("SCALEKIT_RESOURCE_METADATA_URL environment variable not set")
        if not self.SCALEKIT_AUTHORIZATION_SERVERS:
            raise ValueError("SCALEKIT_AUTHORIZATION_SERVERS environment variable not set")
        if not self.SCALEKIT_AUDIENCE_NAME:
            raise ValueError("SCALEKIT_AUDIENCE_NAME environment variable not set")

settings = Settings()