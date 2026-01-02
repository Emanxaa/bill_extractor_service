from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
from pathlib import Path
import pytesseract


class Settings(BaseSettings):
    APP_NAME: str = "Bill Extractor"
    ENV: str = "dev"
    UPLOAD_DIR: str = "uploads"

    # Gemini (env name masih GOOGLE_API_KEY)
    GEMINI_API_KEY: Optional[str] = Field(
        default=None,
        validation_alias="GOOGLE_API_KEY"
    )

    class Config:
        env_file = ".env"


settings = Settings()


# OCR config (explicit)
TESSERACT_CMD = Path(
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)
pytesseract.pytesseract.tesseract_cmd = str(TESSERACT_CMD)
