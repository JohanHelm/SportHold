from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from datetime import date, datetime, timedelta
from app.domain.helpers.enums import SlotType, DaysOfWeek, ScheduleStatus


# вся киллер фича - тут
class SlotModel(BaseModel):
    status: Optional[int] = Field(default=ScheduleStatus.INACTIVE)
    started: Optional[datetime] = Field(default=datetime.now())
    ended: Optional[datetime] = Field(default=date.today() + timedelta(minutes=30))
    created: Optional[datetime] = Field(default=datetime.now())
    type: Optional[int] = Field(default=SlotType.ACCESSIBLE)

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class SlotData(BaseModel):
    slots: List[SlotModel]

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
