from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from datetime import date, datetime, timedelta, time
from app.domain.helpers.enums import SlotType, DaysOfWeek, ScheduleStatus


# вся киллер фича - тут
class ScheduleModel(BaseModel):
    id: Optional[int] = Field()
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    mask_days: Optional[int] = Field(default=DaysOfWeek.ALL)
    status: Optional[int] = Field(default=ScheduleStatus.INACTIVE)
    started: Optional[datetime] = Field(default=date.today())
    ended: Optional[datetime] = Field(default=date.today() + timedelta(days=30))
    created: Optional[datetime] = Field(default=date.today())
    slot_type: Optional[int] = Field(default=SlotType.ACCESSIBLE)
    slot_time: Optional[int] = Field(None, ge=1, le=1440)
    hour_start: Optional[time] = Field(default=time(9))
    hour_end: Optional[time] = Field(default=time(18))

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    def __hash__(self) -> int:  # change to FROZEN pydantic
        return self.name.__hash__()  # or self.id.__hash__()

class ScheduleData(BaseModel):
    schedules: List[ScheduleModel]