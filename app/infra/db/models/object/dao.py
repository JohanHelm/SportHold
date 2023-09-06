from app.domain.models.object.dto import ObjectCreate, ObjectGet
from app.infra.db.models.object.schema import Object


class ObjectDAO:
    def __init__(self, session):
        self.session = session

    async def create(self, _object: ObjectCreate):
        sa_object_add: Object = Object(**_object.model_dump())
        async with self.session() as session:
            session.add(sa_object_add)
            await session.commit()
            get_object_pydantic = ObjectGet.model_validate(sa_object_add)
            print(get_object_pydantic)
            return get_object_pydantic
    #
    # async def get_by_id(self, id):
    #     async with self.session() as session:
    #         user = await session.get(User, id)
    #         get_user_pydantic = UserGet.model_validate(user)
    #         return get_user_pydantic
    #
    # async def update(self, updated_user: UserGet):
    #     async with self.session() as session:
    #         user = await session.get(User, updated_user.id)
    #         kv = updated_user.model_dump()
    #         for key, value in kv.items():
    #             setattr(user, key, value)
    #         await session.commit()
    #         get_user_pydantic = UserGet.model_validate(user)
    #         return get_user_pydantic
    #
    #
