import asyncio
from typing import Dict, Any, Optional
from .base_agent import BaseAgent
from integrations.llm import OpenRouterClient

class MarketingAgent(BaseAgent):
    """
    Агент для маркетингового анализа и генерации структуры продукта (использует OpenRouter).
    """
    
    @property
    def stage_name(self) -> str:
        return 'marketing'

    async def run(self, input_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Запускает маркетингового агента для создания структуры.
        """
        self.log("Начало работы маркетингового агента (Генерация через AI)")
        input_data = input_data or {}
        
        try:
            video_url = input_data.get('video_url', '')
            context = ""
            if video_url:
                context = f"Учитывай контекст продукта, связанный с видео: {video_url}"
                
            llm = OpenRouterClient()
            prompt = f"""
            Сгенерируй маркетинговую стратегию для инфопродукта на тему 'Рост дохода и автоворонки для бизнеса/экспертов'.
            {context}
            Ответ должен быть СТРОГО в формате JSON с ключами:
            - "hero_offer": строка (мощный, цепляющий оффер для главного экрана, до 10 слов)
            - "pain_points": массив строк (3 главные боли целевой аудитории)
            - "key_messages": массив строк (5 ключевых выгод или тезисов продукта)
            - "landing_structure": объект с ключами "target_audience" и "mechanics" (массив из 3 механик)
            
            Важно: верни только JSON, без форматирования markdown.
            """
            
            self.log("Отправка запроса к нейросети (OpenRouter)...")
            output_data = await llm.generate_json(prompt)
            
            # Фолбэк, если ключа нет или вернулась ошибка
            if not output_data:
                self.log("Нейросеть вернула пустой ответ. Использую дефолтные значения (Mock).")
                output_data = {
                    "hero_offer": "Верни 30% потерянных денег из воронки",
                    "pain_points": [
                        "Потеря денег в воронке (брошенные платежи)",
                        "Отток лидов без системы восстановления",
                        "Низкий средний чек (нет допродаж)"
                    ],
                    "key_messages": [
                        "Каждый брошенный платеж — это ваши недозаработанные деньги.",
                        "Автоматизация восстановления лидов экономит до 20 часов в неделю.",
                        "Допродажи могут увеличить выручку на 30% без затрат на рекламу.",
                        "Восстановление корзин — самый дешевый способ получения прибыли.",
                        "Персонализированные предложения повышают конверсию на 40%."
                    ],
                    "landing_structure": {
                        "target_audience": "Предприниматели и продюсеры онлайн-школ",
                        "mechanics": ["Автоматический дожим", "Апселлы", "Сбор базы"]
                    }
                }
            
            self.save_output(output_data, f"{self.stage_name}_output.json")
            self.log("Работа маркетингового агента успешно завершена")
            return output_data
            
        except Exception as e:
            self.log(f"Произошла ошибка при выполнении маркетингового анализа: {e}", level="ERROR")
            return {}
