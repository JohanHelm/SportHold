from pydantic import BaseModel, ConfigDict
from datetime import date, time, timedelta
from typing import Optional, List


class SlotBase(BaseModel):
    schedule_id: Optional[int] = None
    start_date: date
    start_time: time
    timedelta: timedelta
    user_id_deque: List[int]

    model_config = ConfigDict(from_attributes=True)


class SlotCreate(SlotBase):
    ...


class SlotGet(SlotBase):
    id: int
