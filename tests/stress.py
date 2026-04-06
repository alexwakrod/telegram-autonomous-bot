import asyncio
from telethon import TelegramClient
import os

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

async def send_cmd(cmd):
    async with TelegramClient('stress', api_id, api_hash).start(bot_token=bot_token) as client:
        await client.send_message('me', cmd)

async def stress():
    tasks = [send_cmd('/help') for _ in range(150)]
    await asyncio.gather(*tasks)

asyncio.run(stress())