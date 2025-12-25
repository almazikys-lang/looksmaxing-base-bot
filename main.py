#!/usr/bin/env python3
import os, sys, json, asyncio, re, logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
if not BOT_TOKEN:
    print("[ERROR] BOT_TOKEN not set!")
    sys.exit(1)

try:
    with open('sections.json') as f:
        SECTIONS = {s['id']: s for s in json.load(f)}
except:
    SECTIONS = {}

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

def txt(h):
    return re.sub(r'<[^<]+?>', '', h).strip()

def menu():
    buttons = [
        [InlineKeyboardButton(text="🏛️ ATLAS", callback_data="s_atlas")],
        [InlineKeyboardButton(text="📐 V-Figure", callback_data="s_figure")],
        [InlineKeyboardButton(text="❤️ Health", callback_data="s_health")],
        [InlineKeyboardButton(text="💀 Bonesmashing", callback_data="s_bonesmashing")],
        [InlineKeyboardButton(text="👄 Mewing", callback_data="s_mew")],
        [InlineKeyboardButton(text="💪 Training", callback_data="s_training")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@dp.message(CommandStart())
async def start(message: types.Message):
    text = "🎯 **Looksmaxing Base Bot v2.0**\n\n"
    text += "Выбери раздел для изучения:\n"
    await message.answer(text, parse_mode="Markdown", reply_markup=menu())
    logger.info(f"User {message.from_user.id} started bot")

@dp.callback_query(F.data.startswith('s_'))
async def section(callback: types.CallbackQuery):
    section_id = callback.data[2:]
    
    if section_id not in SECTIONS:
        await callback.answer("❌ Раздел не найден", show_alert=True)
        return
    
    section_data = SECTIONS[section_id]
    content = txt(section_data.get('html', ''))
    
    if not content:
        content = "📝 Контент скоро будет доступен..."
    
    chunks = []
    while len(content) > 3500:
        p = content.rfind('\n', 0, 3500)
        if p == -1:
            p = 3500
        chunks.append(content[:p])
        content = content[p:].lstrip()
    if content:
        chunks.append(content)
    
    await callback.message.edit_text(f"📖 **{section_data.get('name', section_id)}**\n\n{chunks[0] if chunks else 'Нет содержимого'}")
    
    for i, chunk in enumerate(chunks[1:], 1):
        await asyncio.sleep(0.5)
        await callback.message.answer(chunk, parse_mode="Markdown")
    
    back_button = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="back")]])
    await callback.message.answer("\n", reply_markup=back_button)
    await callback.answer()
    logger.info(f"User {callback.from_user.id} viewed section: {section_id}")

@dp.callback_query(F.data == "back")
async def back(callback: types.CallbackQuery):
    text = "🎯 **Looksmaxing Base Bot v2.0**\n\nВыбери раздел для изучения:"
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=menu())
    await callback.answer()

@dp.message()
async def echo(message: types.Message):
    await message.answer("ℹ️ Используй /start для начала", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="📖 Меню", callback_data="back")]]))

async def main():
    logger.info("🤖 Бот запущен в режиме polling...")
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
