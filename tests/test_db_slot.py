import datetime
from typing import List

import pytest
from app.domain.models.slot.dto import SlotCreate, SlotGet
from app.infra.db.models.slot.dao import SlotDAO
from collections import deque
from datetime import date, time, timedelta

pytest_plugins = ('pytest_asyncio',)

PK_ID = None


@pytest.mark.asyncio
async def test_slot_add(async_db_session):
    session = await async_db_session
    slot_dao = SlotDAO(session)

    slot_as_deque = deque()
    slot_as_deque.append("1")
    slot_as_deque.append("2")
    slot_as_list = list(slot_as_deque)
    slot_deque_as_str = ','.join(slot_as_list)

    test_slot_pydantic = SlotCreate(
        schedule_id=123,
        start_date=date(
            year=2023,
            month=10,
            day=1
        ),
        start_time=time(hour=10, minute=1),
        timedelta=timedelta(minutes=30),
        user_id_deque=slot_deque_as_str
    )
    created_slot: SlotGet = await slot_dao.create(test_slot_pydantic)
    returned_deque_as_str = created_slot.user_id_deque
    returned_deque = deque()
    returned_deque.extend(returned_deque_as_str.split(","))

    assert slot_as_deque == returned_deque
