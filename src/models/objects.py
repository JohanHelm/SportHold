from pydantic import BaseModel
from schedules import BaseSchedule
from typing import List


class BaseObject(BaseModel):
    name: str = None
    desc: str = None
    schedules: List[BaseSchedule] = None
