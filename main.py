#!/usr/bin/env python3
import os, sys, json, asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    print("ERROR: BOT_TOKEN not set")
    sys.exit(1)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

try:
    with open('sections.json', 'r', encoding='utf-8') as f:
        SECTIONS = {s['id']: s for s in json.load(f)}
except:
    SECTIONS = {}

def txt(h):
    import re
    return re.sub(r'<[^<]+?>', '', h).strip()

@dp.message(CommandStart())
async def start(message: types.Message):
    kb = [[InlineKeyboardButton(text="🏛️ ATLAS", callback_data="s_atlas")]]
    kb.append([InlineKeyboardButton(text="📐 V-Figure", callback_data="s_figure")])
    kb.append([InlineKeyboardButton(text="❤️ Health", callback_data="s_health")])
    kb.append([InlineKeyboardButton(text="💀 Bonesmashing", callback_data="s_bonesmashing")])
    kb.append([InlineKeyboardButton(text="👄 Mewing", callback_data="s_mew")])
    kb.append([InlineKeyboardButton(text="💪 Training", callback_data="s_training")])
    await message.answer("🎯 Menu:", reply_markup=InlineKeyboardMarkup(inline_keyboard=kb))

@dp.callback_query(F.data.startswith('s_'))
async def show_section(callback: types.CallbackQuery):
    sid = callback.data[2:]
    if sid not in SECTIONS:
        await callback.answer("Not found", show_alert=True)
        return
    s = SECTIONS[sid]
    await callback.message.edit_text(txt(s.get('html', 'No content')))
    await callback.answer()

@dp.message()
async def any_msg(message: types.Message):
    await message.answer("/start")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
