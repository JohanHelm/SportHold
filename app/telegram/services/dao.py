"""
                     Data Access Object (DAO)

 Всегда выделяется часть кода, модуль, отвечающающий за передачу
  запросов в БД и обработку полученных от  неё ответов.  В общем
  случае, определение   Data Access Object  описывает  его   как
  прослойку  между  БД  и  системой. DAO  абстрагирует  сущности
  системы и делает их отображение на БД, определяет общие методы
  использования соединения, его  получение,  закрытие  и   (или)
  возвращение в Connection Pool.

"""

import logging
from typing import NoReturn, Union

from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.infra.db.sqlite.models.user import User

logger = logging.getLogger(__name__)


class DataAccessObject:
    def __init__(self, session: AsyncSession) -> NoReturn:
        self.session: AsyncSession = session

    #  Get object with type model 'db_object' from id
    async def get_object(self, db_object: Union[User], db_object_id: int = None) -> list:
        statement = select(db_object)
        if db_object_id:
            statement = statement.where(db_object.id == db_object_id)

        result: Result = await self.session.execute(statement)
        return [item.to_dict for item in result.scalars().all()]

    #  Merge object
    async def add_object(self, db_object: Union[User]) -> None:
        await self.session.merge(db_object)
