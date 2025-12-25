#!/usr/bin/env python3
import os,sys,json,asyncio,re
from aiogram import Bot,Dispatcher,types,F
from aiogram.types import InlineKeyboardButton as IKB,InlineKeyboardMarkup as IKM
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler,setup_application
from aiohttp import web
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN","")
if not BOT_TOKEN:
    print("[ERROR] BOT_TOKEN not set!")
    sys.exit(1)

try:
    with open('sections.json') as f:
        SECTIONS={s['id']:s for s in json.load(f)}
except:
    SECTIONS={}

bot=Bot(token=BOT_TOKEN)
dp=Dispatcher(storage=MemoryStorage())

def txt(h):return re.sub('<[^<]+?>','',h).strip()
def menu():
    return IKM(inline_keyboard=[[IKB(text=f,callback_data=f"s_{d}")] for d,f in [('atlas','🏛️ ATLAS'),('figure','📐 V-Figure'),('health','❤️ Health'),('bonesmashing','💀 Bonesmashing'),('mew','👄 Mewing'),('training','💪 Training'),('close','❌ Close')]])

@dp.message(CommandStart())
async def start(m:types.Message):
    await m.answer("🎯 **Looksmaxing Base Bot**\n\nSelect:",parse_mode="Markdown",reply_markup=menu())

@dp.callback_query(F.data.startswith('s_'))
async def section(c:types.CallbackQuery):
    sid=c.data[2:]
    if sid=='close':
        await c.message.delete()
        return await c.answer()
    if sid not in SECTIONS:
        return await c.answer("Not found",show_alert=True)
    s=SECTIONS[sid]
    t=txt(s.get('html',''))
    if not t:t=f"Content coming soon..."
    chunks=[]
    while len(t)>3500:
        p=t.rfind('\n',0,3500)
        if p==-1:p=3500
        chunks.append(t[:p])
        t=t[p:].lstrip()
    if t:chunks.append(t)
    for i,ch in enumerate(chunks):
        kb=IKM(inline_keyboard=[[IKB(text="⬅️ Back",callback_data="back")]]) if i==len(chunks)-1 else None
        await c.message.answer(ch,parse_mode="Markdown",reply_markup=kb)
        await asyncio.sleep(0.1)
    await c.answer()

@dp.callback_query(F.data=="back")
async def back(c:types.CallbackQuery):
    await c.message.answer("🎯 Menu:",parse_mode="Markdown",reply_markup=menu())
    await c.answer()

@dp.message()
async def echo(m:types.Message):
    await m.answer("Use /start",reply_markup=IKM(inline_keyboard=[[IKB(text="Menu",callback_data="back")]]))

async def on_startup(application):
    webhook_url=os.getenv('WEBHOOK_URL',f'https://looksmaxing-base-bot.onrender.com')
    await bot.set_webhook(url=webhook_url+'/webhook')
    print(f"[BOT] Webhook set to {webhook_url}/webhook")

async def on_shutdown(application):
    await bot.session.close()

def main():
    app=web.Application()
    
    wh_requests_handler=SimpleRequestHandler(dispatcher=dp,bot=bot)
    wh_requests_handler.register(app,path="/webhook")
    setup_application(app,dp,bot=bot,on_startup=on_startup,on_shutdown=on_shutdown)
    
    app.router.add_get('/',lambda r:web.Response(text='Bot OK'))
    
    web.run_app(app,host='0.0.0.0',port=int(os.getenv('PORT','10000')))

if __name__=='__main__':
    main()
