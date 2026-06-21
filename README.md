# 🤖 Telegram Autonomous Bot – High Concurrency, Reminders, Fuzzing

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://python.org)
[![Telethon](https://img.shields.io/badge/Telethon-1.36%2B-green)](https://docs.telethon.dev)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Asyncpg-blue)](https://www.postgresql.org)
[![Fuzzing](https://img.shields.io/badge/Hypothesis-AFL-orange)](https://hypothesis.works)

An **autonomous, production‑ready Telegram bot** built with **Telethon**.  
Handles **≥100 concurrent updates**, per‑user rate limiting, scheduled reminders (DM), command logging, and **continuous fuzzing integration** (Hypothesis + AFL).  
Packaged as **Snap** and **Flatpak** for Linux desktop.

## ✨ Features

- ⚡ **High concurrency** – async Telethon, handles 100+ events simultaneously.
- ⏲️ **Per‑user rate limiting** – sliding window (5 commands / 10 sec).
- ⏰ **Reminder system** – set reminders via `/remind`, get DM notifications.
- 📊 **Command logging** – all commands stored in PostgreSQL (shared with dashboard).
- 🔥 **Continuous fuzzing** – Hypothesis property‑based tests + AFL harness.
- 📦 **Snap / Flatpak** – easy desktop installation (recipes included).
- 🛡️ **Error resilient** – automatic retries, graceful shutdown.

## 🚀 Quick Start (Local)

### Prerequisites
- Python 3.11+
- PostgreSQL 14+ (shared with dashboard)
- Telegram API credentials ([my.telegram.org](https://my.telegram.org))

### Setup
```bash
git clone https://github.com/lelextb/telegram-autonomous-bot.git
cd telegram-autonomous-bot
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill API_ID, API_HASH, BOT_TOKEN, DATABASE_URL
python -m bot.main
```

### Database
The bot expects a PostgreSQL database with tables:
- `command_logs`
- `reminders`
- `moderation_rules`

Run the migrations from the [dashboard repository](https://github.com/alexwakrod/telegram-bot-analytics-dashboard).

## 🧪 Fuzzing
```bash
# Hypothesis fuzzing
python -m bot.main --fuzz

# AFL++ (requires afl‑gcc)
afl-fuzz -i fuzzing/inputs -o fuzzing/findings -- python fuzzing/afl_harness.py @@
```

## 📦 Packaging
- **Snap**: `snapcraft` → `sudo snap install --dangerous telegram-bot_*.snap`
- **Flatpak**: `flatpak-builder build-dir flatpak/org.example.bot.yml --force-clean`

## 🐳 Docker (optional)
```bash
docker build -t telegram-bot .
docker run --env-file .env telegram-bot
```

## 📈 Integration with Dashboard
The bot writes to the same PostgreSQL database used by the [dashboard](https://github.com/alexwakrod/telegram-bot-analytics-dashboard).  
Once the dashboard is running, you will see:
- Command heatmap
- Hourly analytics
- Active reminders (cancel from dashboard)
- Moderation rules (bot reads them automatically)

## 📝 License
MIT – free to use and modify.
