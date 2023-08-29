from datetime import date, time, timedelta
from typing import List
from pydantic import BaseModel

from src.models.queues import BaseQueue


class BaseSlot(BaseModel):
    start_date: date
    start_time: time
    timedelta: timedelta
    queue: List[BaseQueue]
