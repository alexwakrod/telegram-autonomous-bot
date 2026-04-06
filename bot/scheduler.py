import asyncio
from datetime import datetime
from bot.models import AsyncSessionLocal, Reminder
from bot.client import client
from sqlalchemy import select, update

async def reminder_loop():
    while True:
        await asyncio.sleep(5)
        async with AsyncSessionLocal() as session:
            now = datetime.utcnow()
            stmt = select(Reminder).where(Reminder.remind_at <= now, Reminder.done == False)
            reminders = (await session.execute(stmt)).scalars().all()
            for r in reminders:
                try:
                    await client.send_message(r.user_id, f"⏰ Reminder: {r.message}")
                    await session.execute(update(Reminder).where(Reminder.id == r.id).values(done=True))
                    await session.commit()
                except Exception as e:
                    print(f"Reminder failed for user {r.user_id}: {e}")