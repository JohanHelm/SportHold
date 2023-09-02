from datetime import time, timedelta, datetime
import random
from pprint import pprint

from app.domain.models.users import BaseUser
from app.domain.models.objects import BaseObject
from app.domain.models import BaseSchedule

from app.infra.db import UserController
from app.infra.db import ObjectController
from app.infra.db import SchedulesController
from app.infra.db import SlotsController

from app.infra.db import InMemoryDB

db = InMemoryDB

user_control = UserController(db)
object_control = ObjectController(db)
schedule_control = SchedulesController(db)
slot_control = SlotsController(db)


def test_create_retvive_user():
    # создаем пользователя, создаем объект
    # для объекта делаем расписание, генерируем слоты
    #
    #
    test_user_model = BaseUser(fname="Evgeniy", lname="Borshev", tg_id=19884123)
    saved_user = user_control.save_user(user=test_user_model)

    test_object_model = BaseObject(name="Jet 2nd floor table tennis", desc="Simple ping-pong table", schedules=[])
    test_object = object_control.save_object(test_object_model)

    test_schedule_model = BaseSchedule(name="Test Schedule", days_open=["all"], open_from=time(8, 0, 0),
                                       open_until=time(20, 0, 0), min_book_time=timedelta(minutes=15),
                                       max_book_time=timedelta(minutes=30), time_step=timedelta(minutes=15))
    test_schedule = schedule_control.save_schedule(test_schedule_model)

    slots = schedule_control.generate_slots(
        uuid=test_schedule.id, interval=timedelta(hours=2), dt_from=datetime(2023, 10, 1, 9, 21)
    )

    user_slot_choice = random.choice(slots)

    slot = slot_control.create_slot(test_schedule.id, datetime_started=user_slot_choice, dt=timedelta(minutes=30))
    slot = slot_control.slot_add_member_to_queue(slot, saved_user)
    slot_control.save_slot(slot)

    pprint(db.DATABASE)