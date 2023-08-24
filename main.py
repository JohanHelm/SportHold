# Start telegram bot
import asyncio
from src.telegram.bot import start_bot

if __name__ == "__main__":
    asyncio.run(start_bot())
