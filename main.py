import asyncio
import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN or BOT_TOKEN == "":
    logger.warning("⚠️ BOT_TOKEN is empty or not set!")
    BOT_TOKEN = "0:0"
    logger.info("⚠️ Using dummy token for startup testing")
else:
    logger.info(f"✅ BOT_TOKEN loaded successfully (length={len(BOT_TOKEN)})")

try:
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    logger.info("✅ Bot object created successfully")
except Exception as e:
    logger.error(f"❌ Failed to create bot: {e}")
    raise

@dp.message(Command("start"))
async def start_handler(message: Message):
    logger.info(f"📨 /start command from user {message.from_user.id}")
    try:
        await message.answer("🎯 Добро пожаловать в Looksmaxing Base Bot!")
        logger.info("✅ Message sent successfully")
    except Exception as e:
        logger.error(f"❌ Error sending message: {e}")

@dp.message(Command("help"))
async def help_handler(message: Message):
    help_text = "/start - Start\n/help - Help\n/menu - Menu"
    await message.answer(help_text)

@dp.message()
async def echo_handler(message: Message):
    logger.info(f"📨 Message from {message.from_user.id}: {message.text}")
    try:
        await message.answer(f"Вы написали: {message.text}")
    except Exception as e:
        logger.error(f"❌ Error: {e}")

async def main():
    logger.info("")
    logger.info("="*60)
    logger.info("🤖 LOOKSMAXING BASE BOT STARTING")
    logger.info("="*60)
    logger.info("")
    
    try:
        if BOT_TOKEN == "0:0":
            logger.warning("⚠️  Using dummy token - bot is in test mode")
            logger.info("⚠️  Waiting for messages... (bot will not respond in test mode)")
            # Just keep the bot running in test mode
            while True:
                await asyncio.sleep(60)
                logger.info("🔄 Bot still running (test mode)...")
        else:
            logger.info("🚀 Starting polling with real Telegram...")
            await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logger.error(f"❌ Fatal error in bot: {type(e).__name__}: {e}")
        logger.exception("Full traceback:")
        raise
    finally:
        logger.info("🛑 Shutting down...")
        if BOT_TOKEN != "0:0":
            await bot.session.close()
        logger.info("👋 Bot stopped")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("⏹️  Bot interrupted by user")
    except Exception as e:
        logger.critical(f"💥 CRITICAL ERROR: {e}")
        logger.exception("Full traceback:")
        raise
