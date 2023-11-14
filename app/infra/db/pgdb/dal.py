from contextlib import asynccontextmanager
from loguru import logger
from sqlalchemy import Engine, event

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

class Builder:
    def __init__(self, uri: str, echo: bool):
        self.engine = create_async_engine(url=uri, echo=echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False
        )

        @event.listens_for(Engine, "before_cursor_execute")
        def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            logger.debug("SQL: Executing: \n{} \nParameters: {}".format(statement, parameters))

        @event.listens_for(Engine, "handle_error")
        def handle_exception(context):
            logger.exception("SQL: Exception occurred", exc_info=context.original_exception)

    @asynccontextmanager
    async def get_session(self) -> AsyncSession:
        async with self.session_factory() as session:
            try:
                yield session
            finally:
                await session.close()
