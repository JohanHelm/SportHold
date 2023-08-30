from typing import List
from datetime import time, timedelta
from uuid import UUID, uuid4

from pydantic import BaseModel, Field



class BaseSchedule(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str = None
    days_open: List = []
    open_from: time = None
    open_until: time = None
    min_book_time: timedelta = None
    max_book_time: timedelta = None
    time_step: timedelta = None
