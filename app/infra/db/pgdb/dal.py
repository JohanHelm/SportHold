from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

SYNC_DATABASE_URL = "postgresql+psycopg2://postgres:qwerty123@127.0.0.1:5432/dev"
ASYNC_DATABASE_URL = "postgresql+asyncpg:///postgres:qwerty123@127.0.0.1:5432/dev"


class Builder:
    def __init__(self, uri: str, echo: bool):
        self.engine = create_async_engine(url=uri, echo=echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False
        )

    @asynccontextmanager
    async def get_session(self) -> AsyncSession:
        async with self.session_factory() as session:
            try:
                yield session
            finally:
                await session.close()
