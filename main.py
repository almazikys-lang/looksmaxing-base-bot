import asyncio
import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    logger.error("BOT_TOKEN environment variable not found!")
    raise RuntimeError("BOT_TOKEN not found in environment")

logger.info(f"Bot token loaded (len={len(BOT_TOKEN)})")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: Message):
    logger.info(f"Start command from {message.from_user.id}")
    await message.answer("Привет! Я - Looksmaxing Base Bot")

@dp.message(Command("help"))
async def help_handler(message: Message):
    help_text = "/start - Restart\n/help - Help\n/menu - Menu"
    await message.answer(help_text)

@dp.message(Command("menu"))
async def menu_handler(message: Message):
    menu_text = "MENU"
    await message.answer(menu_text)

@dp.message()
async def echo_handler(message: Message):
    logger.info(f"Message from {message.from_user.id}: {message.text}")
    await message.answer(f"You said: {message.text}")

async def main():
    logger.info("========== BOT STARTING ==========")
    try:
        logger.info("Attempting to get bot info...")
        me = await bot.get_me()
        logger.info(f"Bot authenticated: {me.username}")
        
        logger.info("Starting polling...")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logger.error(f"Error in main: {type(e).__name__}: {str(e)}")
        logger.exception("Full traceback:")
        raise
    finally:
        logger.info("Closing bot session...")
        await bot.session.close()
        logger.info("Bot stopped")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot interrupted by user")
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
        raise
