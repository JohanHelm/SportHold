from sqlalchemy import select
from sqlalchemy import update

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

    async def get_by_id(self, id):
        async with self.session() as session:
            user = await session.get(User, id)
            get_user_pydantic = UserGet.model_validate(user)
            return get_user_pydantic

    async def update(self, updated_user: UserGet):
        async with self.session() as session:
            user = await session.get(User, updated_user.id)
            kv = updated_user.model_dump()
            for key, value in kv.items():
                setattr(user, key, value)
            await session.commit()
            get_user_pydantic = UserGet.model_validate(user)
            return get_user_pydantic


