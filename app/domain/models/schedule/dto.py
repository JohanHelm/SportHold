from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date
from app.helpers.maskers.weekdays import DaysOfWeek
from app.helpers.maskers.weeks import WeeksInYear
from app.helpers.maskers.quartals import Quartals
from app.helpers.maskers.daysmonth import DaysInMonth

class ScheduleBase(BaseModel):
    name: Optional[str]
    description: Optional[str]
    status: str
    valid_from: date
    valid_to: date
    mask_weekdays: DaysOfWeek
    mask_weeks: WeeksInYear
    mask_quratals: Quartals
    mask_days_month: DaysInMonth
    mask_days_year:
    nth_weekday: DaysOfWeek
    nth_index: int
    slot_type:
    slot_min_time: int
    slot_max_time: int
    slot_step_time: int
    hour_start: int
    hour_end: int
    policy_merge:
    policy_suggest:
    
    rental_id: int

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class ScheduleCreate(ScheduleBase):
    ...


class ScheduleGet(ScheduleBase):
    id: int
