#!/usr/bin/env python3
import os
import sys
import json
import logging
import asyncio
from typing import List
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiohttp import web
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(name)s: %(message)s')
logger = logging.getLogger(__name__)

print(f"[BOOT] Python {sys.version}")
BOT_TOKEN = os.getenv("BOT_TOKEN", "NOT_SET")
if BOT_TOKEN == "NOT_SET":
    logger.error("[BOOT] BOT_TOKEN not set!")
    sys.exit(1)
print(f"[BOOT] BOT_TOKEN loaded")

# Load sections
try:
    with open('sections.json', 'r', encoding='utf-8') as f:
        SECTIONS = {s['id']: s for s in json.load(f)}
        logger.info(f"[BOOT] Loaded {len(SECTIONS)} sections")
except:
    logger.warning("[BOOT] sections.json not found")
    SECTIONS = {}

def extract_text(html: str) -> str:
    import re
    return re.sub('<[^<]+?>', '', html).strip()

def chunk_text(text: str, max_len: int = 3500) -> List[str]:
    chunks = []
    while len(text) > max_len:
        split_pos = text.rfind('\n', 0, max_len)
        if split_pos == -1:
            split_pos = max_len
        chunks.append(text[:split_pos])
        text = text[split_pos:].lstrip()
    if text:
        chunks.append(text)
    return chunks

storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=storage)

def build_menu() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="🏛️ ATLAS", callback_data="section_atlas")],
        [InlineKeyboardButton(text="📐 V-Figure", callback_data="section_figure")],
        [InlineKeyboardButton(text="❤️ Health", callback_data="section_health")],
        [InlineKeyboardButton(text="💀 Bonesmashing", callback_data="section_bonesmashing")],
        [InlineKeyboardButton(text="👄 Mewing", callback_data="section_mew")],
        [InlineKeyboardButton(text="💪 Training", callback_data="section_training")],
        [InlineKeyboardButton(text="❌ Close", callback_data="close_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@dp.message(CommandStart())
async def start(message: types.Message):
    logger.info(f"[USER] {message.from_user.id} started bot")
    await message.answer(
        "🎯 **Looksmaxing Base Bot v2.0**\n\nYour guide to maxing out. Select a section:",
        parse_mode="Markdown",
        reply_markup=build_menu()
    )

@dp.callback_query(F.data.startswith("section_"))
async def handle_section(callback: types.CallbackQuery):
    section_id = callback.data.replace("section_", "")
    if section_id not in SECTIONS:
        await callback.answer("Not found", show_alert=True)
        return
    
    section = SECTIONS[section_id]
    text = extract_text(section.get('html', ''))
    if not text:
        text = f"📖 {section['title']}\n\nContent coming soon..."
    
    chunks = chunk_text(text)
    logger.info(f"[USER] {callback.from_user.id} requested {section_id}")
    
    for i, chunk in enumerate(chunks):
        if i == len(chunks) - 1:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ Back", callback_data="back_menu")]])
            await callback.message.answer(chunk, parse_mode="Markdown", reply_markup=keyboard)
        else:
            await callback.message.answer(chunk, parse_mode="Markdown")
        await asyncio.sleep(0.1)
    
    await callback.answer()

@dp.callback_query(F.data == "back_menu")
async def back_menu(callback: types.CallbackQuery):
    logger.info(f"[USER] {callback.from_user.id} back to menu")
    await callback.message.answer("🎯 **Menu**\n\nSelect:", parse_mode="Markdown", reply_markup=build_menu())
    await callback.answer()

@dp.callback_query(F.data == "close_menu")
async def close_menu(callback: types.CallbackQuery):
    logger.info(f"[USER] {callback.from_user.id} closed")
    await callback.message.delete()
    await callback.answer()

@dp.message()
async def unknown(message: types.Message):
    logger.info(f"[MSG] {message.from_user.id}: {message.text}")
    await message.answer("👋 Use /start", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🏠 Menu", callback_data="back_menu")]]))

async def health_check(request):
    return web.Response(text="Looksmaxing Base Bot is running!")

async def start_http():
    app = web.Application()
    app.router.add_get('/', health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 10000)
    await site.start()
    logger.info("[HTTP] Server on port 10000")
    return runner

async def main():
    logger.info(f"[BOT] Starting with token: {BOT_TOKEN[:10]}...")
    try:
        http_runner = await start_http()
        logger.info("[BOT] Polling started")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logger.error(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    print("[BOOT] Starting Looksmaxing Base Bot v2.0...")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Bot stopped")
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
