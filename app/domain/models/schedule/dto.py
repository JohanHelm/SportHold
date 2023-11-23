from sqlalchemy.types import JSON
from pydantic import BaseModel, ConfigDict
from typing import Optional


class ScheduleBase(BaseModel):
    description: Optional[str]
    status: str
    conditions: JSON
    rental_id: int

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class ScheduleCreate(ScheduleBase):
    ...


class ScheduleGet(ScheduleBase):
    id: int
