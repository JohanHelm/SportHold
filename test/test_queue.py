import datetime
from datetime import timedelta

from app.domain.models.user.dto import BaseUser
from app.domain.models.slots import BaseSlot
from app.infra.db import SlotsController
from app.infra.db import UserController
from app.infra.db import InMemoryDB
from uuid import uuid4

db = InMemoryDB
slot_control = SlotsController(db)
user_control = UserController(db)

def test_regular_slot_adding_member():
    result_slot: BaseSlot = slot_control.create_slot(
        uuid4(),
        datetime.datetime(
            year=2023, month=10, day=1,
            hour=6, minute=30
        ),
        dt=timedelta(minutes=15)
    )

    user = BaseUser(
        fname="test fname",
        lname="test lname",
        tg_id=123
    )

    user: BaseUser = user_control.save_user(user)

    result_clot = slot_control.slot_add_member_to_queue(result_slot, user)

    result_clot = slot_control.save_slot(result_slot)
    assert result_clot.queue[0].tg_id == user.tg_id

