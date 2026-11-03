"""
Модуль интеграции с Telegram Bot API (aiogram 3.x).
"""
import os
import json
import logging
import asyncio
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from dotenv import load_dotenv
from aiohttp import web

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramInfoBot:
    """Бот для инфопродуктов на базе aiogram 3.x."""

    def __init__(self, token: str) -> None:
        self.bot = Bot(token=token)
        self.dp = Dispatcher()
        self.router = Router()
        self.dp.include_router(self.router)
        self.welcome_message = self._load_welcome_message()
        self.setup_handlers()

    def _load_welcome_message(self) -> str:
        """Загрузка сгенерированного сообщения из пайплайна (copywriting_output.json)."""
        try:
            with open('output/copywriting_output.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("telegram_welcome_message", "Привет! Добро пожаловать в проект.")
        except FileNotFoundError:
            return "Привет! Добро пожаловать! (Сгенерированный текст не найден)"

    def setup_handlers(self) -> None:
        """Регистрация обработчиков."""
        self.router.message(CommandStart())(self.on_start)
        self.router.callback_query()(self.on_callback)

    async def on_start(self, message: Message) -> None:
        """Обработчик команды /start."""
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🚀 Запустить систему", callback_data="info")],
            [InlineKeyboardButton(text="❓ Задать вопрос", callback_data="support")]
        ])
        await message.answer(self.welcome_message, reply_markup=keyboard)

    async def on_callback(self, callback: CallbackQuery) -> None:
        """Обработчик нажатий на инлайн-кнопки."""
        if callback.data == "info":
            await callback.message.answer("Здесь мы можем выдать бонусный материал или ссылку на оплату Prodamus!")
        elif callback.data == "support":
            await callback.message.answer("Напишите ваш вопрос, и наш менеджер скоро ответит.")
        await callback.answer()

    async def run(self) -> None:
        """Запуск поллинга бота."""
        logger.info("Запуск Telegram бота...")
        await self.dp.start_polling(self.bot)

async def health_check(request):
    """Служебный роут для Render, чтобы он понимал, что бот жив."""
    return web.Response(text="Bot is running OK!")

async def main():
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token or token.strip() == "":
        logger.error("TELEGRAM_BOT_TOKEN не задан!")
        return
        
    bot = TelegramInfoBot(token=token)
    
    # Запускаем фиктивный веб-сервер, чтобы Render.com (облако) не выключал бота
    app = web.Application()
    app.router.add_get('/', health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logger.info(f"Служебный веб-сервер запущен на порту {port}")

    await bot.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен.")


# Алиас для обратной совместимости с imports
run_bot = main
