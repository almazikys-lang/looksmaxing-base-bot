#!/usr/bin/env python3
import os, sys, json, asyncio, re, logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    logger.error("BOT_TOKEN environment variable is not set")
    sys.exit(1)

logger.info(f"Bot token length: {len(BOT_TOKEN)}")

try:
    with open('sections.json', 'r', encoding='utf-8') as f:
        SECTIONS = {s['id']: s for s in json.load(f)}
    logger.info(f"Loaded {len(SECTIONS)} sections")
except Exception as e:
    logger.error(f"Error loading sections.json: {e}")
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
    text = "🎯 **Looksmaxing Base Bot v2.0**\n\nВыбери раздел для изучения:\n"
    await message.answer(text, parse_mode="Markdown", reply_markup=menu())
    logger.info(f"User {message.from_user.id} started bot")

@dp.callback_query(F.data.startswith('s_'))
async def section(callback: types.CallbackQuery):
    section_id = callback.data[2:]
    logger.info(f"User {callback.from_user.id} clicked section: {section_id}")
    
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
    
    for i, chunk in enumerate(chunks):
        if i == 0:
            await callback.message.edit_text(f"📖 **{section_data.get('name', section_id)}**\n\n{chunk}")
        else:
            await asyncio.sleep(0.5)
            await callback.message.answer(chunk)
    
    back_btn = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]])
    await callback.message.answer("\n", reply_markup=back_btn)
    await callback.answer()

@dp.callback_query(F.data == "back")
async def back(callback: types.CallbackQuery):
    text = "🎯 **Looksmaxing Base Bot v2.0**\n\nВыбери раздел:"
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=menu())
    await callback.answer()

@dp.message()
async def echo(message: types.Message):
    await message.answer("ℹ️ Используй /start", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Menu", callback_data="back")]]))

async def main():
    logger.info("🤖 Начинаю polling...")
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
