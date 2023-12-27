from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import date, datetime, timedelta
from app.domain.helpers.enums import SlotType, DaysOfWeek, ScheduleStatus


# вся киллер фича - тут
class SlotModel(BaseModel):
    status: Optional[int] = Field(default=ScheduleStatus.INACTIVE)
    started: Optional[datetime] = Field(default=date.today())
    ended: Optional[datetime] = Field(default=date.today() + timedelta(days=30))
    created: Optional[datetime] = Field(default=date.today())
    type: Optional[int] = Field(default=SlotType.ACCESSIBLE)

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
