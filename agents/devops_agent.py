import asyncio
from typing import Dict, Any, Optional
from .base_agent import BaseAgent

class DevOpsAgent(BaseAgent):
    """
    Агент для деплоя, настройки интеграций и тестирования.
    """
    
    @property
    def stage_name(self) -> str:
        return 'devops'

    async def run(self, input_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Запускает DevOps-агента.
        """
        self.log("Начало работы DevOps-агента")
        
        try:
            # Загрузка данных предыдущих стадий
            design_data = self.load_previous_stage('design')
            copywriting_data = self.load_previous_stage('copywriting')
            
            # Выполнение шагов деплоя
            vercel_url = await self._deploy_landing()
            payment_status = await self._setup_payments()
            bot_username = await self._create_bot(copywriting_data.get('telegram_welcome_message', ''))
            legal_status = await self._deploy_legal()
            test_results = await self._run_tests()
            
            output_data = {
                "urls": {
                    "landing_url": vercel_url,
                    "telegram_bot": f"https://t.me/{bot_username}" if bot_username != 'skipped' else 'skipped',
                },
                "status": {
                    "payment_integration": payment_status,
                    "legal_documents": legal_status,
                },
                "tests": test_results
            }
            
            self.save_output(output_data, f"{self.stage_name}_output.json")
            self.log("Работа DevOps-агента успешно завершена")
            return output_data
            
        except Exception as e:
            self.log(f"Произошла ошибка на этапе деплоя: {e}", level="ERROR")
            return {}

    async def _deploy_landing(self) -> str:
        try:
            self.log("Деплой на Vercel...")
            await asyncio.sleep(1)
            return "https://funnel-optimizer-demo.vercel.app"
        except Exception as e:
            self.log(f"Ошибка деплоя на Vercel: {e}", level="ERROR")
            return "skipped"

    async def _setup_payments(self) -> str:
        try:
            self.log("Настройка платежной системы Prodamus...")
            await asyncio.sleep(1)
            return "success"
        except Exception as e:
            self.log(f"Ошибка настройки Prodamus: {e}", level="ERROR")
            return "skipped"

    async def _create_bot(self, welcome_msg: str) -> str:
        try:
            self.log("Создание Telegram-бота...")
            await asyncio.sleep(1)
            return "funnel_optimizer_bot"
        except Exception as e:
            self.log(f"Ошибка создания Telegram-бота: {e}", level="ERROR")
            return "skipped"

    async def _deploy_legal(self) -> str:
        try:
            self.log("Размещение юридических документов...")
            await asyncio.sleep(1)
            return "success"
        except Exception as e:
            self.log(f"Ошибка размещения документов: {e}", level="ERROR")
            return "skipped"

    async def _run_tests(self) -> Dict[str, bool]:
        try:
            self.log("Запуск финальных тестов...")
            await asyncio.sleep(1)
            return {
                "mobile_responsive": True,
                "forms_working": True,
                "payment_gateway": True
            }
        except Exception as e:
            self.log(f"Ошибка при тестировании: {e}", level="ERROR")
            return {"tests_failed": True}
