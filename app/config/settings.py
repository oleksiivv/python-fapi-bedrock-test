import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application settings and configuration"""

    # App settings
    APP_NAME: str = "Image Analysis API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "AI-powered image analysis using Amazon Bedrock"

    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # AWS settings
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")

    # Bedrock settings
    BEDROCK_MODEL_ID: str = os.getenv(
        "BEDROCK_MODEL_ID",
        "anthropic.claude-3-sonnet-20240229-v1:0"
    )
    BEDROCK_MAX_TOKENS: int = int(os.getenv("BEDROCK_MAX_TOKENS", "1000"))

    # File upload settings
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "5"))
    MAX_FILE_SIZE_BYTES: int = MAX_FILE_SIZE_MB * 1024 * 1024
    ALLOWED_EXTENSIONS: List[str] = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"]
    ALLOWED_CONTENT_TYPES: List[str] = [
        "image/jpeg", "image/png", "image/gif",
        "image/bmp", "image/webp"
    ]

    # Default prompts
    DEFAULT_ANALYSIS_PROMPT: str = "Analyze this image and describe what you see in detail."

    @property
    def max_file_size_mb(self) -> int:
        return self.MAX_FILE_SIZE_MB


# Global settings instance
settings = Settings()