from app.domain.models.schedule.dto import ScheduleCreate, ScheduleGet
from app.infra.db.models.schedule.schema import Schedule
from sqlalchemy.future import select


class ScheduleDAO:
    async def create(self, session, schedule: ScheduleCreate):
        sa_schedule_add: Schedule = Schedule(**schedule.model_dump())
        async with session() as session:
            session.add(sa_schedule_add)
            await session.commit()
        get_schedule_pydantic: ScheduleGet = ScheduleGet.model_validate(sa_schedule_add)
        return get_schedule_pydantic

    async def show_rentals_schedule(self, session, rental_id):
        async with session() as session:
            result = await session.execute(select(Schedule).where(Schedule.rental_id == rental_id))
            schedule = result.scalars().all()
        return schedule
