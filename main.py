#!/usr/bin/env python3
import os,sys,json,logging,asyncio
from aiogram import Bot,Dispatcher,types,F
from aiogram.types import InlineKeyboardButton as IKB,InlineKeyboardMarkup as IKM
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiohttp import web
from dotenv import load_dotenv
import re

load_dotenv()
logging.basicConfig(level=logging.INFO,format='%(message)s')
logger = logging.getLogger()

BOT_TOKEN = os.getenv("BOT_TOKEN","NOT_SET")
if BOT_TOKEN == "NOT_SET":
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

async def handle_update(request):
    data=await request.json()
    update=types.Update(**data)
    await dp.feed_update(bot,update)
    return web.Response()

async def health(r):return web.Response(text="Bot OK")

async def main():
    app=web.Application()
    app.router.add_post('/webhook',handle_update)
    app.router.add_get('/',health)
    
    runner=web.AppRunner(app)
    await runner.setup()
    site=web.TCPSite(runner,'0.0.0.0',int(os.getenv('PORT','10000')))
    await site.start()
    
    try:
        webhook_url=os.getenv('WEBHOOK_URL',f'https://looksmaxing-base-bot.onrender.com')
await bot.set_webhook(url=webhook_url+'/webhook')
        print(f"[BOT] Webhook set to {webhook_url}/webhook")
        print(f"[BOT] Web server on port {os.getenv('PORT','10000')}")
        while True:
            await asyncio.sleep(60)
    except Exception as e:
        print(f"[ERROR] {e}")
        await runner.cleanup()
        sys.exit(1)

if __name__=="__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("[SHUTDOWN] Bot stopped")
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
