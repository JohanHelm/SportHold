# Start telegram bot
import asyncio
from app.telegram.bot import start_bot

if __name__ == "__main__":
    asyncio.run(start_bot())
