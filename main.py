import asyncio
import json
import logging
import os
import re

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not found in .env")

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

with open("sections.json", "r", encoding="utf-8") as f:
    SECTIONS = json.load(f)

SECTION_BY_ID = {s["id"]: s for s in SECTIONS}

def build_main_menu() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="🏑 ATLAS", callback_data="section:atlas"),
            InlineKeyboardButton(text="📏 V-фигура", callback_data="section:vfigure")
        ],
        [
            InlineKeyboardButton(text="❤️ Health", callback_data="section:health"),
            InlineKeyboardButton(text="🚹 Bonesmashing", callback_data="section:bonesmash")
        ],
        [
            InlineKeyboardButton(text="🗣️ Mewing", callback_data="section:mew"),
            InlineKeyboardButton(text="💪 Training", callback_data="section:training")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def html_to_telegram_text(html: str) -> str:
    text = re.sub(r"<br\s*/?>
?", "\n", html)
    text = re.sub(r"</p>", "\n\n", text)
    text = re.sub(r"<p[^>]*>", "", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r" +", " ", text)
    return text.strip()

async def send_section(chat_id: int, section_id: str):
    section = SECTION_BY_ID.get(section_id)
    if not section:
        await bot.send_message(chat_id, "Section not found.")
        return
    text = html_to_telegram_text(section["html"])
    MAX_LEN = 3500
    parts = [text[i:i + MAX_LEN] for i in range(0, len(text), MAX_LEN)]
    header = f"<b>\ud83d\udd39 {section['title']}</b>\n\n"
    if parts:
        await bot.send_message(chat_id, header + parts[0])
        for part in parts[1:]:
            await bot.send_message(chat_id, part)
    else:
        await bot.send_message(chat_id, header + "Section is empty.")

@dp.message(CommandStart())
async def cmd_start(message: Message):
    text = (
        "\ud83d\udc4b <b>Welcome to LOOKSMAXING BASE v2.0!</b>\n\n"
        "Select a section from the menu below \ud83d\udc47"
    )
    await message.answer(text, reply_markup=build_main_menu())

@dp.callback_query(F.data.startswith("section:"))
async def handle_section_callback(callback: CallbackQuery):
    section_id = callback.data.split(":", 1)[1]
    await callback.answer()
    await send_section(callback.message.chat.id, section_id)

@dp.message()
async def handle_any_message(message: Message):
    await message.answer(
        "ℹ️ Please use the menu buttons to navigate.\n\n"
        "Type /start to return to the main menu."
    )

async def main():
    logger.info("🤖 Bot started...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
