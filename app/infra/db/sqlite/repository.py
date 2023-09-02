from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy import create_engine, MetaData

# ASYNC_DATABASE_URL = "sqlite+aiosqlite:///app.db"
SYNC_DATABASE_URL = "sqlite+pysqlite:///app.db"

# async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)
sync_engine = create_engine(SYNC_DATABASE_URL, echo=True)

Base = declarative_base()

# async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
sync_session = Session(sync_engine)

# async def get_session() -> AsyncSession:
#     async with async_session() as session:
#         yield session

metadata = MetaData()
metadata.create_all(bind=sync_engine)
