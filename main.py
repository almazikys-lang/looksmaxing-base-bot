#!/usr/bin/env python3
import os,asyncio,json,re
from aiogram import Bot,Dispatcher,types,F
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage

token=os.environ.get("BOT_TOKEN")
bot=Bot(token=token)
dp=Dispatcher(storage=MemoryStorage())

try:
    with open('sections.json','r',encoding='utf-8') as f:
        SECTIONS={s['id']:s for s in json.load(f)}
except:
    SECTIONS={}

def txt(h):
    return re.sub(r'<[^<]+?>','',h).strip()

@dp.message(CommandStart())
async def start(m:types.Message):
    kb=[[InlineKeyboardButton(text=f"🏛️ {s.get('name','')}",callback_data=f"s_{sid}")] for sid,s in list(SECTIONS.items())]
    await m.answer("🎯 Выбери раздел:",reply_markup=InlineKeyboardMarkup(inline_keyboard=kb))

@dp.callback_query(F.data.startswith('s_'))
async def section(c:types.CallbackQuery):
    sid=c.data[2:]
    if sid not in SECTIONS:return await c.answer("Не найдено",show_alert=True)
    s=SECTIONS[sid]
    ct=txt(s.get('html','Нет контента'))
    if len(ct)>3000:ct=ct[:3000]+"..."
    kb=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ Назад",callback_data="back")]])
    await c.message.edit_text(ct,reply_markup=kb)
    await c.answer()

@dp.callback_query(F.data=="back")
async def back(c:types.CallbackQuery):
    kb=[[InlineKeyboardButton(text=f"🏛️ {s.get('name','')}",callback_data=f"s_{sid}")] for sid,s in list(SECTIONS.items())]
    await c.message.edit_text("🎯 Выбери раздел:",reply_markup=InlineKeyboardMarkup(inline_keyboard=kb))
    await c.answer()

@dp.message()
async def any_msg(m:types.Message):
    await m.answer("/start для меню")

async def main():
    await dp.start_polling(bot)

if __name__=="__main__":
    asyncio.run(main())
