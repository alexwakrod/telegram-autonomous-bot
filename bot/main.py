import asyncio
from bot.client import client, BOT_TOKEN
from bot.scheduler import reminder_loop
from bot.handlers import commands   # registers handlers

async def main():
    await client.start(bot_token=BOT_TOKEN)
    asyncio.create_task(reminder_loop())
    print("🤖 Bot started. Awaiting updates...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())