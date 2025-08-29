import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    UPLOAD_DIR: str = "uploads"
    AUDIO_DIR: str = "audio_output"
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS: list = [".mp4", ".avi", ".mov", ".mkv", ".webm"]

settings = Settings()