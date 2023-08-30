from datetime import date, time, timedelta
from typing import List

from pydantic import BaseModel, UUID4, Field
from uuid import UUID, uuid4

from src.models.users import BaseUser


class BaseSlot(BaseModel):
    schedule_id: UUID4
    id: UUID = Field(default_factory=uuid4)
    start_date: date
    start_time: time
    timedelta: timedelta
    queue: List[BaseUser]
