"""
Интеграционные модули для пайплайна инфопродукта.
"""
from .prodamus import ProdamusClient
from .telegram_bot import TelegramInfoBot, run_bot
from .google_sheets import SheetsDB
from .vercel_deploy import VercelDeployer
from .whisper_transcribe import WhisperTranscriber

__all__ = [
    "ProdamusClient",
    "TelegramInfoBot",
    "run_bot",
    "SheetsDB",
    "VercelDeployer",
    "WhisperTranscriber"
]
