from app.domain.models.slot.dto import SlotCreate, SlotGet
from app.infra.db.models.slot.schema import Slot


class SlotDAO:
    def __init__(self, session):
        self.session = session

    async def create(self, slot: SlotCreate):
        sa_slot_add: Slot = Slot(**slot.model_dump())
        async with self.session() as session:
            session.add(sa_slot_add)
            await session.commit()
            get_slot_pydantic = SlotGet.model_validate(sa_slot_add)
            print(get_slot_pydantic)
            return get_slot_pydantic
    # #
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
