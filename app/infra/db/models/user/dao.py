from app.domain.models.user.dto import UserCreate, UserGet
from app.infra.db.models.user.schema import User


class UsedDAO:
    async def create(self, session, user: UserCreate):
        sa_user_add: User = User(**user.model_dump())
        async with session() as session:
            session.add(sa_user_add)
            await session.commit()
        get_user_pydantic = UserGet.model_validate(sa_user_add)
        return get_user_pydantic

    async def get_by_id(self, session, id):
        async with session() as session:
            user = await session.get(User, id)
        get_user_pydantic = UserGet.model_validate(user)
        return get_user_pydantic

    async def update(self, session, updated_user: UserGet):
        async with session() as session:
            user = await session.get(User, updated_user.id)
            kv = updated_user.model_dump()
            for key, value in kv.items():
                setattr(user, key, value)
            await session.commit()
        get_user_pydantic = UserGet.model_validate(user)
        return get_user_pydantic

    async def get_by_tg_id(self, session, tg_user_id):
        async with session() as session:
            result = await session.execute(User.__table__.select().where(User.user_id == tg_user_id))
            user = result.all()
        return user

    async def user_exists(self, session, tg_user_id):
        return bool(await UsedDAO.get_by_tg_id(self, session, tg_user_id))
