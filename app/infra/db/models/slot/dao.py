from app.domain.models.slot.dto import SlotCreate, SlotGet
from app.infra.db.models.slot.schema import Slot


class SlotDAO:
    async def create(self, session, slot: SlotCreate):
        sa_slot_add: Slot = Slot(**slot.model_dump())
        async with session() as session:
            session.add(sa_slot_add)
            await session.commit()
        get_slot_pydantic = SlotGet.model_validate(sa_slot_add)
        return get_slot_pydantic
