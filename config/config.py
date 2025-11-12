import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).parent.parent

class Config:
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'conversationalist_ai')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')

    STORAGE_PATH = Path(os.getenv('STORAGE_PATH', PROJECT_ROOT / 'storage'))
    AUDIO_PATH = STORAGE_PATH / 'audio'
    VIDEO_PATH = STORAGE_PATH / 'video'
    SNAPSHOTS_PATH = STORAGE_PATH / 'snapshots'

    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    @classmethod
    def get_database_url(cls):
        return f"postgresql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"

config = Config()
