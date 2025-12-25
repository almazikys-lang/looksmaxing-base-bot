# ⚡ Quick Start Guide

## 30-Second Setup

### Step 1: Clone Repository
```bash
git clone https://github.com/almazikys-lang/looksmaxing-base-bot.git
cd looksmaxing-base-bot
```

### Step 2: Create Virtual Environment
**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### Step 3: Update .env with Your Token
Edit `.env` and add your BOT_TOKEN from @BotFather:
```
BOT_TOKEN=your_token_here
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Run the Bot
```bash
python main.py
```

You'll see:
```
INFO:__main__:🤖 Bot started...
```

### Step 6: Test in Telegram
1. Open Telegram
2. Find your bot: **@looksmaxing_base_bot**
3. Send `/start`
4. Click menu buttons and explore!

---

## Troubleshooting

**Q: "BOT_TOKEN not found in .env"**
- Check .env file exists in project root
- Make sure you pasted your token correctly

**Q: "ModuleNotFoundError: No module named 'aiogram'"**
- Activate virtual environment: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`

**Q: Bot doesn't respond**
- Make sure bot is running (check console)
- Make sure .env has valid BOT_TOKEN
- Wait 1-2 seconds, then try again

---

For detailed setup, see [README.md](README.md)
