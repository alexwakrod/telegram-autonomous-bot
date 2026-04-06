import asyncio
import signal
from bot.client import client, BOT_TOKEN
from bot.scheduler import reminder_loop
from bot.handlers import commands   # registers handlers

async def main():
    # Start the client
    await client.start(bot_token=BOT_TOKEN)
    # Start reminder loop as background task
    reminder_task = asyncio.create_task(reminder_loop())
    print("🤖 Bot started. Awaiting updates... Press Ctrl+C to stop.")

    # Set up signal handlers for graceful shutdown
    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()

    def signal_handler():
        print("\n🛑 Shutting down gracefully...")
        stop_event.set()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, signal_handler)

    # Wait until stop signal received
    await stop_event.wait()

    # Cancel reminder task and disconnect client
    reminder_task.cancel()
    await client.disconnect()
    print("✅ Bot stopped.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Already handled by signal, but just in case
        pass