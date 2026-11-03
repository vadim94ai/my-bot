import asyncio
import json
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
        config = input_data.get('config', {})
        if not config:
            try:
                with open('configs/project_config.json', 'r', encoding='utf-8') as f:
                    config = json.load(f)
            except Exception:
                config = {}
                
        project_name = config.get('project_name', 'Обучение по генерации AI-видео с нуля')
        product_desc = config.get('product_description', 'Генерация видео, персонажи, промты, автоматизации, Claude/Antigravity, 3D Blender, AI-мультфильмы')
        target_audience = config.get('target_audience', 'новички в нейросетях, контент-мейкеры, рилсмейкеры')
        price = config.get('price', 3000)
        
        try:
            llm = OpenRouterClient()
            prompt = f"""
            Сгенерируй мощную маркетинговую стратегию для инфопродукта:
            Название: {project_name}
            Программа/содержание: {product_desc}
            Целевая аудитория: {target_audience}
            Стоимость: {price} рублей.
            
            Ответ должен быть СТРОГО в формате JSON с ключами:
            - "hero_offer": строка (мощный, цепляющий оффер для первого экрана, до 10-12 слов)
            - "pain_points": массив из 3 строк (главные боли аудитории: например, страх сложных программ, блокировки зарубежных сервисов/оплат, нет идей/персонажей)
            - "key_messages": массив из 5 строк (ключевые выгоды и результаты студента)
            - "landing_structure": объект с ключами "target_audience" и "mechanics" (массив из 3-4 ключевых модулей/направлений обучения)
            
            Важно: верни только валидный JSON, без маркдаун тегов и без пояснений.
            """
            
            self.log("Отправка запроса к нейросети (OpenRouter)...")
            output_data = await llm.generate_json(prompt)
            
            # Фолбэк, если нейросеть недоступна
            if not output_data:
                self.log("Нейросеть вернула пустой ответ. Использую качественные значения по умолчанию.")
                output_data = {
                    "hero_offer": "Научись создавать трендовые AI-видео и мультфильмы с нуля за 7 дней",
                    "pain_points": [
                        "Непонятно, как оплачивать зарубежные нейросети и обходить блокировки из РФ",
                        "Персонажи меняют лицо в каждом кадре, а картинка выглядит дерганой и неестественной",
                        "Сложно разобраться в монтаже, моушене и связках нейросетей без технических навыков"
                    ],
                    "key_messages": [
                        "Пошаговый гайд по оплате и настройке всех топ-нейросетей без риска блокировок",
                        "Секретные промты для фиксации лиц и создания стабильных консистентных персонажей",
                        "Создание анимаций, моушен-графики и живых каруселей в Claude и Antigravity",
                        "Комбинация Blender 3D + AI для создания голливудской картинки и мультфильмов",
                        "Готовые автоматизации пайплайнов для экономии 90% времени при монтаже Reels и Shorts"
                    ],
                    "landing_structure": {
                        "target_audience": target_audience,
                        "mechanics": [
                            "Доступ к сервисам и генерация стабильных персонажей",
                            "Моушен-графика, Claude/Antigravity и живые карусели",
                            "Blender 3D + AI мультфильмы и полный продакшн"
                        ]
                    }
                }
            
            self.save_output(output_data, f"{self.stage_name}_output.json")
            self.log("Работа маркетингового агента успешно завершена")
            return output_data
            
        except Exception as e:
            self.log(f"Произошла ошибка в маркетинговом агенте: {e}", level="ERROR")
            return {}
