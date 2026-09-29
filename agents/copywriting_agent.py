import asyncio
from typing import Dict, Any, Optional
from .base_agent import BaseAgent
from integrations.llm import OpenRouterClient

class CopywritingAgent(BaseAgent):
    """
    Агент для написания продающих текстов (использует OpenRouter).
    """
    
    @property
    def stage_name(self) -> str:
        return 'copywriting'

    async def run(self, input_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Запускает агента копирайтера.
        """
        self.log("Начало работы агента копирайтера (Генерация через AI)")
        
        try:
            marketing_data = self.load_previous_stage('marketing')
            if not marketing_data:
                self.log("Маркетинговые данные не найдены, используются дефолтные", level="WARNING")
                marketing_data = {"hero_offer": "Курс по увеличению прибыли"}

            llm = OpenRouterClient()
            offer = marketing_data.get('hero_offer', 'Секреты роста продаж')
            pains = marketing_data.get('pain_points', [])
            
            prompt = f"""
            Ты — профессиональный копирайтер. Напиши тексты для лендинга на основе оффера: "{offer}"
            Боли аудитории: {', '.join(pains) if pains else 'Мало продаж, дорогие лиды'}.
            
            Верни СТРОГО JSON со следующими ключами:
            - "landing_h1": строка (главный заголовок сайта)
            - "landing_h2": строка (подзаголовок, раскрывающий ценность)
            - "hero_paragraph": строка (абзац текста под заголовком)
            - "mechanics": массив из 3 объектов, у каждого ключи "title" и "description"
            - "faq": массив из 3 частых вопросов-ответов, объекты с ключами "question" и "answer"
            - "telegram_welcome_message": приветственное сообщение для бота (с эмодзи)
            
            Важно: верни только валидный JSON.
            """
            
            self.log("Отправка запроса копирайтера к нейросети (OpenRouter)...")
            output_data = await llm.generate_json(prompt)
            
            if not output_data:
                self.log("Нейросеть вернула пустой ответ. Использую дефолтные значения (Mock).")
                output_data = {
                    "landing_h1": "Верни 30% потерянных денег из воронки продаж",
                    "landing_h2": "Внедри автоматическую систему возврата клиентов.",
                    "hero_paragraph": "Каждый день вы теряете клиентов, которые уже готовы были купить...",
                    "mechanics": [
                        {"title": "Верни брошенные платежи", "description": "Мы настроим триггерные рассылки..."},
                        {"title": "Увеличь средний чек", "description": "Автоматические допродажи сразу после покупки..."},
                        {"title": "Собери базу контактов", "description": "Преврати анонимный трафик в лояльную аудиторию..."}
                    ],
                    "faq": [
                        {"question": "Как быстро я увижу результаты?", "answer": "Обычно в течение 48 часов."},
                        {"question": "Нужно ли мне менять CRM?", "answer": "Нет, система интегрируется со всеми."},
                        {"question": "Какая окупаемость?", "answer": "В среднем 1.5 месяца."}
                    ],
                    "telegram_welcome_message": "Привет! 👋 Добро пожаловать в нашего бота."
                }
            
            # Сохраняем скрипт для Reels (всегда дефолт для стабильности)
            output_data["reels_script"] = {
                "0-20s": "Каждый день 30% ваших клиентов уходят на этапе оплаты...",
                "20-50s": "Проблема не в вашем продукте, а в отсутствии системы возврата...",
                "50-60s": "Переходи по ссылке в описании, чтобы получить бесплатный аудит."
            }
            
            self.save_output(output_data, f"{self.stage_name}_output.json")
            self.log("Работа агента копирайтера успешно завершена")
            return output_data
            
        except Exception as e:
            self.log(f"Произошла ошибка при генерации текстов: {e}", level="ERROR")
            return {}
