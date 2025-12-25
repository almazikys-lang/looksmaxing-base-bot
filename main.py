#!/usr/bin/env python3
import os,asyncio
from aiogram import Bot,Dispatcher,types,F
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup

token=os.environ.get("BOT_TOKEN")
bot=Bot(token=token)
dp=Dispatcher(storage=MemoryStorage())

@dp.message(CommandStart())
async def start(m:types.Message):
 await m.answer("Hello!")

@dp.message()
async def msg(m:types.Message):
 await m.answer("Hi")

async def main():
 await dp.start_polling(bot)

if __name__=="__main__":
 asyncio.run(main())
