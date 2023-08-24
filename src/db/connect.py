import logging

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
)

logger = logging.getLogger(__name__)

Base = declarative_base()


async def create_async_engine_db(url: str, echo: bool) -> AsyncEngine:
    return create_async_engine(url, echo=echo)


async def async_connection_db(engine: AsyncEngine, expire_on_commit: bool) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine=engine, expire_on_commit=expire_on_commit)
