# import pytest
# from app.domain.models.schedule.dto import ScheduleGet, ScheduleCreate
# from app.infra.db.models.schedule.dao import ScheduleDAO
#
# pytest_plugins = ('pytest_asyncio',)
#
#
# @pytest.mark.asyncio
# async def test_schedule_add(session, test_schedule: ScheduleCreate):
#     schedule_dao = ScheduleDAO()
#     created_schedule: ScheduleGet = await schedule_dao.create(session, test_schedule)
#     assert created_schedule.name == test_schedule.name
