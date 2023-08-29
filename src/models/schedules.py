from typing import List
from datetime import time, timedelta
from pydantic import BaseModel

from slots import BaseSlot


class BaseSchedule(BaseModel):
    working_days: List = []
    open_from: time = None
    open_until: time = None
    min_book_time: timedelta = None
    max_book_time: timedelta = None
    time_grid: List = None
    slots: List[BaseSlot] = None
