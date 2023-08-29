from datetime import date, time, timedelta
from typing import List
from pydantic import BaseModel

from queues import BaseQueue


class BaseSlot(BaseModel):
    start_date: date = None
    start_time: time = None
    timedelta: timedelta = None
    queue: List[BaseQueue] = None
