import asyncio
import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not found in .env")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Привет! Я Looksmaxing Base Bot. Напиши /help для справки.")

@dp.message(Command("help"))
async def help_handler(message: Message):
    help_text = """
    /start - Начать
    /help - Справка
    /menu - Главное меню
    """
    await message.answer(help_text)

@dp.message(Command("menu"))
async def menu_handler(message: Message):
    menu_text = """
    🎯 Looksmaxing Base v2.0\n    1. Atlas\n    2. V-Shape\n    3. Health\n    4. Bonesmashing\n    5. Mewing
    """
    await message.answer(menu_text)

@dp.message()
async def echo_handler(message: Message):
    await message.answer(f"Вы написали: {message.text}")

async def main():
    logger.info("Bot started")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
