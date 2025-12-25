# looksmaxing-base-bot 🤖

**Telegram bot for LOOKSMAXING BASE v2.0** - Complete guide with interactive menu

A fully functional Telegram bot that delivers comprehensive looksmaxing education directly through the Telegram interface.

## Features ✨

- 📱 Interactive inline keyboard menu
- 📚 Multiple sections covering:
  - 🏛️ ATLAS (Facial Anatomy)
  - 📐 V-Figure Body Shape
  - ❤️ Health & Longevity
  - 💀 Bonesmashing
  - 👄 Mewing
  - 💪 Physical Training
- 📝 Automatic text formatting and chunking
- 🔒 Secure token management via .env

## Setup Instructions 🚀

### Prerequisites
- Python 3.10+
- Telegram account
- Terminal/Command Prompt

### 1. Get Your Bot Token

1. Open Telegram
2. Search for `@BotFather`
3. Send `/newbot`
4. Follow instructions and get your **BOT_TOKEN**
5. Copy the token

### 2. Clone or Download

```bash
git clone https://github.com/almazikys-lang/looksmaxing-base-bot.git
cd looksmaxing-base-bot
```

### 3. Setup Environment

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### 4. Configure .env

Edit `.env` file:
```
BOT_TOKEN=your_token_here
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Bot

```bash
python main.py
```

You should see:
```
INFO:__main__:🤖 Bot started...
```

### 7. Test Your Bot

1. Open Telegram
2. Find your bot by username (set in BotFather)
3. Send `/start`
4. Click menu buttons and explore sections

## File Structure 📁

```
looksmaxing-base-bot/
├── .env                    # Token configuration
├── main.py                 # Bot logic
├── sections.json           # Content database
├── requirements.txt        # Dependencies
├── README.md              # This file
└── .gitignore             # Git ignore rules
```

## Customization 🎨

### Add More Sections

Edit `sections.json`:

```json
{
  "id": "your_section",
  "title": "Your Section Title",
  "html": "<h2>Your Content</h2><p>Your text here</p>"
}
```

Add button in `main.py` `build_main_menu()` function

## Dependencies 📦

- **aiogram 3.0.0** - Telegram Bot API framework
- **python-dotenv 1.0.0** - Environment variable management

## Deployment 🌐

### Option 1: VPS (Recommended for 24/7)

1. Rent a Linux VPS (Hetzner, Contabo, etc.)
2. Install Python 3.10+
3. Clone repository
4. Set .env with BOT_TOKEN
5. Use systemd service or tmux for persistent running

### Option 2: Heroku/Cloud Platform

Support for cloud deployment coming soon.

## Troubleshooting 🔧

**Bot won't start:**
- Check BOT_TOKEN in .env
- Verify token is valid from BotFather
- Check Python version (3.10+)

**Missing sections:**
- Verify sections.json is in same directory as main.py
- Check JSON formatting is valid

**Long messages cut off:**
- Bot automatically chunks messages >3500 characters
- All content will be delivered in multiple messages

## Contributing 🤝

Contributions welcome! Feel free to:
- Add more sections
- Improve content
- Fix bugs
- Submit pull requests

## License 📄

Open source project

## Support 💬

For issues, questions, or suggestions:
- Open a GitHub issue
- Contact via Telegram

---

**Made with ❤️ for the looksmaxing community**
