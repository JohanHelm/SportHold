from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import date
from app.helpers.maskers.weekdays import DaysOfWeek
from app.helpers.maskers.weeks import WeeksInYear
from app.helpers.maskers.quartals import Quartals
from app.helpers.maskers.daysmonth import DaysInMonth

class ScheduleBase(BaseModel):
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    status: Optional[str] = Field(default=None)
    valid_from: Optional[date] = Field(default=None)
    valid_to: Optional[str] = Field(default=None)
    mask_weekdays: Optional[DaysOfWeek] = Field(default=DaysOfWeek.ALL) 
    mask_weeks: Optional[WeeksInYear] = Field(default=WeeksInYear.ALL)
    mask_quratals: Optional[Quartals] = Field(default=Quartals.ALL)
    mask_days_month: Optional[DaysInMonth] = Field(default=None)
    nth_weekday: Optional[DaysOfWeek] = Field(default=None)
    nth_index: Optional[int] = Field(None, ge=1, le=31)
    slot_type: Optional[str] = Field(default=None)
    slot_min_time: Optional[int] = Field(None, ge=1, le=1440)
    slot_max_time: Optional[int] = Field(None, ge=1, le=1440)
    slot_step_time: Optional[int] = Field(None, ge=1, le=1440)
    hour_start: Optional[int] = Field(None, ge=0, le=24)
    hour_end: Optional[int] = Field(None, ge=0, le=24)
    policy_merge: Optional[str] = Field(default="REGULAR")
    policy_suggest: Optional[str] = Field(default="REGULAR")
    
    rental_id: int

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class ScheduleCreate(ScheduleBase):
    ...


class ScheduleGet(ScheduleBase):
    id: int
