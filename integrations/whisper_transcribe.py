"""
Модуль для транскрибации аудио/видео с использованием OpenAI Whisper.
"""
import os
import re
import logging
from typing import Dict, Any, List
import httpx
from openai import AsyncOpenAI

logger = logging.getLogger(__name__)

class WhisperTranscriber:
    """Класс для транскрибации медиафайлов через Whisper."""

    def __init__(self, api_key: str) -> None:
        """
        Инициализация клиента OpenAI.
        
        :param api_key: API ключ OpenAI
        """
        self.api_key = api_key
        self.client = AsyncOpenAI(api_key=api_key)

    async def download_video(self, url: str, output_path: str = 'temp_video.mp4') -> str:
        """
        Скачивание видео по ссылке.
        
        :param url: Прямая ссылка на файл
        :param output_path: Куда сохранить
        :return: Путь к сохраненному файлу
        """
        logger.info(f"Скачивание файла с {url} в {output_path}")
        async with httpx.AsyncClient(follow_redirects=True) as client:
            async with client.stream("GET", url) as response:
                response.raise_for_status()
                with open(output_path, "wb") as f:
                    async for chunk in response.aiter_bytes():
                        f.write(chunk)
        return output_path

    def _extract_key_points(self, transcript: str, count: int = 15) -> List[str]:
        """
        Извлечение ключевых фраз (предложений) из текста. Упрощенная логика.
        
        :param transcript: Полный текст транскрипции
        :param count: Максимальное количество фраз
        :return: Список ключевых предложений
        """
        sentences = re.split(r'(?<=[.!?]) +', transcript.strip())
        sentences = [s for s in sentences if len(s) > 20]
        
        return sentences[:count]

    async def transcribe(self, file_path: str = '', url: str = '') -> Dict[str, Any]:
        """
        Транскрибация файла. Если передан URL - сначала скачивает файл.
        
        :param file_path: Локальный путь к аудио/видео файлу
        :param url: URL медиафайла
        :return: Словарь с текстом, сегментами и метаданными
        """
        downloaded = False
        target_path = file_path
        
        if url and not file_path:
            target_path = await self.download_video(url)
            downloaded = True
            
        if not target_path or not os.path.exists(target_path):
            raise FileNotFoundError("Медиафайл не найден для транскрибации.")

        logger.info(f"Начало транскрибации файла {target_path}")
        try:
            with open(target_path, "rb") as audio_file:
                # Используем verbose_json для получения сегментов и длительности
                response = await self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="verbose_json"
                )
                
            result = {
                "text": response.text,
                "segments": response.segments,
                "duration": response.duration,
                "language": response.language
            }
            return result
            
        finally:
            if downloaded and os.path.exists(target_path):
                os.remove(target_path)
