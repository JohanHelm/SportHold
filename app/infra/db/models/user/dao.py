from sqlalchemy import select

from app.domain.models.user.dto import UserCreate, UserGet
from app.infra.db.models.user.schema import User


class UsedDAO:
    def __init__(self, session):
        self.session = session

    async def create(self, user: UserCreate):
        sa_user_add: User = User(**user.model_dump())
        async with self.session() as session:
            session.add(sa_user_add)
            await session.commit()
            get_user_pydantic = UserGet.model_validate(sa_user_add)
            print(get_user_pydantic)
            return get_user_pydantic

    async def get(self, filter ):
        async with self.session() as session:
            result = await session.scalars(select(User).filter_by(**filter))
            first_user_in_db = result.first()
            print(first_user_in_db)
            get_user_pydantic = UserGet.model_validate(first_user_in_db)
            return get_user_pydantic