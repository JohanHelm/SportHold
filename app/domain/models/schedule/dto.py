from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import time, timedelta


class ScheduleBase(BaseModel):
    name: Optional[str]
    desc: Optional[str]
    days_open: List[int]
    open_from: time = None
    open_until: time = None
    min_book_time: timedelta = None
    max_book_time: timedelta = None
    time_step: timedelta = None

    model_config = ConfigDict(from_attributes=True)


class ScheduleCreate(ScheduleBase):
    ...


class ScheduleGet(ScheduleBase):
    id: int
