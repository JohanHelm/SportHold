from app.domain.models.schedule.dto import ScheduleCreate,ScheduleGet
from app.infra.db.models.schedule.schema import Schedule


class ScheduleDAO:
    def __init__(self, session):
        self.session = session

    async def create(self, schedule: ScheduleCreate):
        sa_schedule_add: Schedule = Schedule(**schedule.model_dump())
        async with self.session() as session:
            session.add(sa_schedule_add)
            await session.commit()
            get_schedule_pydantic = ScheduleGet.model_validate(sa_schedule_add)
            return get_schedule_pydantic
