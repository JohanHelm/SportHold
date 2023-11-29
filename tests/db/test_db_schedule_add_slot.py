# from datetime import time, timedelta, date
#
# import pytest
# from sqlalchemy import select
# from sqlalchemy.orm import noload
# from sqlalchemy.orm import selectinload
#
# from app.domain.models.schedule.dto import ScheduleGet, ScheduleCreate
# from app.domain.models.slot.controller import QueueController
# from app.domain.models.slot.dto import SlotCreate, SlotGet
# from app.infra.db.models.schedule.dao import ScheduleDAO
# from app.infra.db.models.slot.dao import SlotDAO
# from app.infra.db.models.schedule.schema import Schedule
# from app.infra.db.models.slot.schema import Slot
#
# pytest_plugins = ('pytest_asyncio',)
#
#
# @pytest.mark.asyncio
# async def test_schedule_add(session):
#     schedule_dao = ScheduleDAO()
#     test_schedule_pydantic = ScheduleCreate(
#         name="Test schedule",
#         desc="Description",
#         days_open=[1, 2],
#         open_from=time(9, 0, 0),
#         open_until=time(18, 0, 0),
#         min_book_time=timedelta(minutes=15),
#         max_book_time=timedelta(minutes=30),
#         time_step=timedelta(minutes=15)
#     )
#     created_schedule: ScheduleGet = await schedule_dao.create(session, test_schedule_pydantic)
#     pytest.test_schedule_id = created_schedule.id
#
#     slot_dao = SlotDAO()
#     queue_in = QueueController()
#     users_id_list = [1, 2]
#     data = queue_in.add_list(users_id_list).to_list()
#
#     test_slot_pydantic = SlotCreate(
#         start_date=date(
#             year=2023,
#             month=10,
#             day=1
#         ),
#         start_time=time(hour=10, minute=1),
#         timedelta=timedelta(minutes=30),
#         user_id_deque=data
#     )
#     created_slot: SlotGet = await slot_dao.create(session, test_slot_pydantic)
#     async with session() as session:
#         # optons(selectinload() - https://stackoverflow.com/questions/70104873/how-to-access-relationships-with-async-sqlalchemy
#         sa_scehdule = await session.execute(select(Schedule).where(Schedule.id == created_schedule.id).options(selectinload(Schedule.slot)))
#         sa_scehdule_ = sa_scehdule.scalars().first()
#
#         sa_slot = await session.execute(select(Slot).where(Slot.id == created_slot.id).options(selectinload(Slot.schedule)))
#         sa_slot_ = sa_slot.scalars().first()
#         sa_scehdule_.slot.append(sa_slot_)
#         session.add(sa_scehdule_)
#         await session.commit()
