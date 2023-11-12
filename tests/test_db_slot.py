import pytest
from app.domain.models.slot.dto import SlotCreate, SlotGet
from app.domain.models.slot.controller import QueueController
from app.infra.db.models.slot.dao import SlotDAO
from datetime import date, time, timedelta
from collections import deque

pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
async def test_slot_create(async_db_session):
    session = await async_db_session
    slot_dao = SlotDAO(session)
    queue_in = QueueController()
    queue_out = QueueController()
    users_id_list = [1, 2]
    data = queue_in.add_list(users_id_list).to_list()

    test_slot_pydantic = SlotCreate(
        start_date=date(
            year=2023,
            month=10,
            day=1
        ),
        start_time=time(hour=10, minute=1),
        timedelta=timedelta(minutes=30),
        user_id_deque=data
    )
    created_slot: SlotGet = await slot_dao.create(test_slot_pydantic)
    returned_deque_from_db = created_slot.user_id_deque
    assert queue_in.get_deque() == queue_out.from_list(returned_deque_from_db).get_deque()



def test_slot_remove_first():
    queue_in = QueueController()
    data = [1,2]
    queue_in.add_list(data)
    queue_in.remove_first()

    assert queue_in.get_deque() == deque([2])

def test_slot_remove_id():
    queue_in = QueueController()
    data = [1,2,3]
    queue_in.add_list(data)
    queue_in.remove(2)

    assert queue_in.get_deque() == deque([1,3])
