from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

SYNC_DATABASE_URL = "postgresql+psycopg2://postgres:qwerty123@127.0.0.1:5432/dev"
ASYNC_DATABASE_URL = "postgresql+asyncpg:///postgres:qwerty123@127.0.0.1:5432/dev"


class Builder:
    def __init__(self, uri: str):
        self.engine = None
        self.session = None
        self.uri = uri
        self.base = declarative_base()

    async def async_db_session(self):
        self.engine = create_async_engine(
            self.uri, pool_size=10, echo=True, max_overflow=10
        )

        self.session = async_sessionmaker(
          self.engine, expire_on_commit=False, class_=AsyncSession, autoflush=False, autocommit=False
        )
        return self.session


