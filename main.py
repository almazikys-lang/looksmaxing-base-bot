#!/usr/bin/env python3
import os
import sys
import json
import logging
from typing import Dict, List
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiohttp import web
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)

print(f"[BOOT] Python version: {sys.version}")
print(f"[BOOT] Loading BOT_TOKEN from environment...")

BOT_TOKEN = os.getenv("BOT_TOKEN", "NOT_SET")
if BOT_TOKEN == "NOT_SET":
    logger.error("[BOOT] BOT_TOKEN not set!")
    sys.exit(1)
print(f"[BOOT] BOT_TOKEN loaded successfully")

# Load sections from JSON
TRY_SECTIONS = {}
try:
    with open('sections.json', 'r', encoding='utf-8') as f:
        SECTIONS_DATA = json.load(f)
        SECTIONS = {section['id']: section for section in SECTIONS_DATA}
        logger.info(f"[BOOT] Loaded {len(SECTIONS)} sections from sections.json")
except FileNotFoundError:
    logger.warning("[BOOT] sections.json not found, using default sections")
    SECTIONS = {
        'atlas': {'id': 'atlas', 'title': 'ATLAS', 'html': '<h2>ATLAS - Facial Anatomy</h2><p>Complete guide to facial anatomy</p>'},
        'figure': {'id': 'figure', 'title': 'V-Figure', 'html': '<h2>V-Figure Body Shape</h2><p>Body development guide</p>'},
        'health': {'id': 'health', 'title': 'Health', 'html': '<h2>Health & Longevity</h2><p>Health and fitness guide</p>'},
        'bonesmashing': {'id': 'bonesmashing', 'title': 'Bonesmashing', 'html': '<h2>Bonesmashing</h2><p>Technique guide</p>'},
        'mew': {'id': 'mew', 'title': 'Mewing', 'html': '<h2>Mewing Posture</h2><p>Posture optimization guide</p>'},
        'training': {'id': 'training', 'title': 'Training', 'html': '<h2>Training Guide</h2><p>Physical training guide</p>'}
    }

def extract_text_from_html(html: str) -> str:
    """Extract plain text from HTML content"""
    import re
    text = re.sub('<[^<]+?>', '', html)
    text = text.replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('&amp;', '&').replace('&quot;', '"')
    return text.strip()

def chunk_text(text: str, max_length: int = 3500) -> List[str]:
    """Split text into chunks for Telegram (max 4096 chars per message)"""
    chunks = []
    while len(text) > max_length:
        # Find last newline before max_length
        split_pos = text.rfind('\n', 0, max_length)
        if split_pos == -1:
            split_pos = max_length
        chunks.append(text[:split_pos])
        text = text[split_pos:].lstrip()
    if text:
        chunks.append(text)
    return chunks

# Initialize bot and dispatcher
storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=storage)

def build_main_menu() -> InlineKeyboardMarkup:
    """Build main menu keyboard"""
    buttons = [
        [InlineKeyboardButton(text="🏛️ ATLAS (Facial Anatomy)", callback_data="section_atlas")],
        [InlineKeyboardButton(text="📐 V-Figure (Body Shape)", callback_data="section_figure")],
        [InlineKeyboardButton(text="❤️ Health & Longevity", callback_data="section_health")],
        [InlineKeyboardButton(text="💀 Bonesmashing", callback_data="section_bonesmashing")],
        [InlineKeyboardButton(text="👄 Mewing (Posture)", callback_data="section_mew")],
        [InlineKeyboardButton(text="💪 Physical Training", callback_data="section_training")],
        [InlineKeyboardButton(text="❌ Close", callback_data="close_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@dp.message(CommandStart())
async def command_start(message: types.Message):
    """Handle /start command"""
    logger.info(f"[USER] {message.from_user.id} started bot")
    
    welcome_text = (
        "🎯 **Welcome to Looksmaxing Base Bot v2.0**\n\n"
        "Your comprehensive guide to maxing out your looks and potential.\n\n"
        "Select a section to learn:"
    )
    
    await message.answer(
        welcome_text,
        parse_mode="Markdown",
        reply_markup=build_main_menu()
    )

@dp.callback_query(F.data.startswith("section_"))
async def handle_section(callback: types.CallbackQuery):
    """Handle section selection"""
    section_id = callback.data.replace("section_", "")
    
    if section_id not in SECTIONS:
        await callback.answer("Section not found", show_alert=True)
        return
    
    section = SECTIONS[section_id]
    text = extract_text_from_html(section.get('html', ''))
    
    if not text:
        text = f"📖 {section['title']}\n\nContent for this section coming soon..."
    
    chunks = chunk_text(text)
    
    logger.info(f"[REQUEST] User {callback.from_user.id} requested section: {section_id} ({len(chunks)} chunks)")
    
    # Send all chunks
    for i, chunk in enumerate(chunks):
        if i == len(chunks) - 1:
            # Last chunk - add back button
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Back to Menu", callback_data="back_menu")]
            ])
            await callback.message.answer(
                chunk,
                parse_mode="Markdown",
                reply_markup=keyboard
            )
        else:
            # Intermediate chunks
            await callback.message.answer(chunk, parse_mode="Markdown")
        await asyncio.sleep(0.1)  # Small delay between messages
    
    await callback.answer()

@dp.callback_query(F.data == "back_menu")
async def handle_back_menu(callback: types.CallbackQuery):
    """Handle back to menu button"""
    logger.info(f"[USER] {callback.from_user.id} returned to menu")
    
    await callback.message.answer(
        "🎯 **Looksmaxing Base Menu**\n\nSelect a section:",
        parse_mode="Markdown",
        reply_markup=build_main_menu()
    )
    await callback.answer()

@dp.callback_query(F.data == "close_menu")
async def handle_close_menu(callback: types.CallbackQuery):
    """Handle close menu button"""
    logger.info(f"[USER] {callback.from_user.id} closed menu")
    await callback.message.delete()
    await callback.answer()

@dp.message()
async def handle_unknown(message: types.Message):
    """Handle unknown messages"""
    logger.info(f"[REQUEST] Unknown message from {message.from_user.id}: {message.text}")
    
    await message.answer(
        "👋 I don't understand that command.\n\n"
        "Use /start to see the menu.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🏠 Main Menu", callback_data="back_menu")]
        ])
    )

async def on_startup(app):
    """Startup handler"""
    logger.info("[BOT] Starting Telegram bot polling...")
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

async def web_handler(request):
    """Simple web handler for Render health checks"""
    return web.Response(text="Looksmaxing Base Bot is running!")

async def main():
    """Main bot function"""
    logger.info(f"[BOT] Starting bot with token: {BOT_TOKEN[:10]}...")
    
    try:
        # Set bot commands
        commands = [
            types.BotCommand(command="start", description="Start the bot"),
            types.BotCommand(command="help", description="Show help"),
        ]
        await bot.set_my_commands(commands)
        
        # Start polling
        logger.info("[BOT] Bot started successfully! Waiting for messages...")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logger.error(f"[ERROR] {e}")
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
