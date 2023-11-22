from sqlalchemy.types import JSON
from pydantic import BaseModel, ConfigDict
from typing import Optional


# class ScheduleBase(BaseModel):
#     name: Optional[str]
#     desc: Optional[str]
#     days_open: List[int]
#     open_from: time = None
#     open_until: time = None
#     min_book_time: timedelta = None
#     max_book_time: timedelta = None
#     time_step: timedelta = None
#     slot: List[SlotGet] = []
#
#     model_config = ConfigDict(from_attributes=True)
#
#
# class ScheduleCreate(ScheduleBase):
#     ...
#
#
# class ScheduleGet(ScheduleBase):
#     id: int


class ScheduleBase(BaseModel):
    description: Optional[str]
    status: str
    conditions: str #JSON  json raise pydantic.errors.PydanticSchemaGenerationError: Unable to generate pydantic-core schema for <class 'sqlalchemy.sql.sqltypes.JSON'>. Set `arbitrary_types_allowed=True` in the model_config to ignore this error or implement `__get_pydantic_core_schema__` on your type to fully support it.
    rental_id: int

    model_config = ConfigDict(from_attributes=True)


class ScheduleCreate(ScheduleBase):
    ...


class ScheduleGet(ScheduleBase):
    id: int
