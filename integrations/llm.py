import os
import json
import logging
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Список бесплатных моделей OpenRouter в порядке приоритета
FREE_MODELS = [
    "google/gemma-2-9b-it:free",
    "meta-llama/llama-3.1-8b-instruct:free",
    "qwen/qwen-2.5-7b-instruct:free",
    "huggingfaceh4/zephyr-7b-beta:free",
    "microsoft/phi-3-mini-128k-instruct:free",
    "qwen/qwen3.8-27b:free",
    "nvidia/nemotron-3.5-lightning:free"
]

class OpenRouterClient:
    """Клиент для работы с моделями через OpenRouter с умным перебором."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            logger.warning("OPENROUTER_API_KEY не установлен. Будет использован заглушечный режим.")
            self.client = None
        else:
            self.client = AsyncOpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.api_key,
                max_retries=0  # Отключаем встроенные ретраи, так как мы делаем их сами со сменой модели
            )

    async def generate_json(self, prompt: str, system_prompt: str = "Вы — профессиональный AI-агент.") -> dict:
        """Генерирует JSON-ответ с помощью OpenRouter, перебирая бесплатные модели."""
        if not self.client:
            logger.warning("Ключ OpenRouter отсутствует, возвращаем пустой словарь (stub).")
            return {}

        messages = [
            {"role": "system", "content": system_prompt + " Отвечай ТОЛЬКО валидным JSON без маркдаун-разметки (без ```json)."},
            {"role": "user", "content": prompt}
        ]

        for model_name in FREE_MODELS:
            logger.info(f"Пробуем бесплатную модель: {model_name}...")
            try:
                response = await self.client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    temperature=0.7
                )
                
                result_text = response.choices[0].message.content.strip()
                
                # Очистка от возможных маркдаун тегов
                if result_text.startswith("```json"):
                    result_text = result_text[7:]
                if result_text.startswith("```"):
                    result_text = result_text[3:]
                if result_text.endswith("```"):
                    result_text = result_text[:-3]
                    
                logger.info(f"Успех! Модель {model_name} отдала текст.")
                return json.loads(result_text.strip())
                
            except Exception as e:
                err_msg = str(e).lower()
                if "429" in err_msg or "too many requests" in err_msg:
                    logger.warning(f"Модель {model_name} сейчас перегружена (429). Идем к следующей...")
                elif "404" in err_msg or "not found" in err_msg:
                    logger.warning(f"Модель {model_name} больше не бесплатна или удалена (404). Идем к следующей...")
                else:
                    logger.error(f"Неизвестная ошибка с {model_name}: {e}")
                    
        logger.error("Все бесплатные модели оказались заняты или недоступны!")
        return {}
