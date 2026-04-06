from telethon import events
from bot.client import client
from bot.rate_limit import rate_limiter
from bot.logger import log_command
from bot.models import AsyncSessionLocal, CommandLog, Reminder
from datetime import datetime, timedelta
import re

HELP_PAGES = [
    "**📘 Page 1/3 – Basic Commands**\n/start – Start the bot\n/help <page> – Show this help\n/remind <time> <message> – Set a reminder\nExample: `/remind 10m Buy milk`",
    "**📙 Page 2/3 – Stats**\n/stats – Your command usage\n/reminders – List your active reminders",
    "**📗 Page 3/3 – Moderation**\n(Admin only) – Rules are read from database."
]

def parse_reminder(text):
    match = re.match(r'^(\d+)([smhd])\s+(.+)$', text.strip())
    if not match:
        return None
    value = int(match.group(1))
    unit = match.group(2)
    msg = match.group(3)
    return value, unit, msg

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    user_id = event.sender_id
    if not rate_limiter.is_allowed(user_id):
        await event.reply("⏳ Slow down!")
        return
    log_command(user_id, event.sender.username, 'start', '')
    await event.reply("Hello! I'm a high‑concurrency bot. Use /help.")

@client.on(events.NewMessage(pattern='/help(?:\\s+(\\d+))?'))
async def help_cmd(event):
    user_id = event.sender_id
    if not rate_limiter.is_allowed(user_id):
        await event.reply("Rate limit exceeded.")
        return
    page = int(event.pattern_match.group(1)) if event.pattern_match.group(1) else 1
    if 1 <= page <= len(HELP_PAGES):
        await event.reply(HELP_PAGES[page-1])
    else:
        await event.reply(f"Invalid page. Use /help 1-{len(HELP_PAGES)}")

@client.on(events.NewMessage(pattern='/remind (.+)'))
async def remind(event):
    user_id = event.sender_id
    if not rate_limiter.is_allowed(user_id):
        await event.reply("Rate limit exceeded.")
        return
    args = event.pattern_match.group(1)
    parsed = parse_reminder(args)
    if not parsed:
        await event.reply("Invalid format. Use: `/remind 10m Your message`")
        return
    value, unit, msg = parsed
    delta = timedelta(seconds=value) if unit == 's' else \
            timedelta(minutes=value) if unit == 'm' else \
            timedelta(hours=value) if unit == 'h' else \
            timedelta(days=value)
    remind_at = datetime.utcnow() + delta
    async with AsyncSessionLocal() as session:
        reminder = Reminder(user_id=user_id, chat_id=event.chat_id, remind_at=remind_at, message=msg)
        session.add(reminder)
        await session.commit()
    log_command(user_id, event.sender.username, 'remind', args)
    await event.reply(f"✅ Reminder set for {remind_at} UTC:\n{msg}")

@client.on(events.NewMessage(pattern='/stats'))
async def stats(event):
    user_id = event.sender_id
    if not rate_limiter.is_allowed(user_id):
        await event.reply("Rate limit exceeded.")
        return
    async with AsyncSessionLocal() as session:
        from sqlalchemy import select, func
        stmt = select(func.count()).where(CommandLog.user_id == user_id)
        count = (await session.execute(stmt)).scalar()
    await event.reply(f"📊 You have used {count} commands since I started.")

@client.on(events.NewMessage(pattern='/reminders'))
async def list_reminders(event):
    user_id = event.sender_id
    if not rate_limiter.is_allowed(user_id):
        await event.reply("Rate limit exceeded.")
        return
    async with AsyncSessionLocal() as session:
        from sqlalchemy import select
        stmt = select(Reminder).where(Reminder.user_id == user_id, Reminder.done == False)
        reminders = (await session.execute(stmt)).scalars().all()
    if not reminders:
        await event.reply("You have no active reminders.")
    else:
        msg = "⏰ **Your reminders:**\n"
        for r in reminders:
            msg += f"- {r.remind_at} UTC: {r.message}\n"
        await event.reply(msg)

# Log every command to database
@client.on(events.NewMessage)
async def log_all_commands(event):
    if event.is_private and event.text and event.text.startswith('/'):
        cmd = event.text.split()[0]
        async with AsyncSessionLocal() as session:
            log_entry = CommandLog(user_id=event.sender_id, command=cmd, timestamp=datetime.utcnow())
            session.add(log_entry)
            await session.commit()