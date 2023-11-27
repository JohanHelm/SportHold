from enum import Enum, auto
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import date, timedelta

from app.helpers.maskers.weekdays import DaysOfWeek
from app.helpers.maskers.weeks import WeeksInYear
from app.helpers.maskers.quartals import Quartals
from app.helpers.maskers.daysmonth import DaysInMonth

from app.domain.models.slot.dto import SlotType


class ScheduleStatus(Enum):
    ACTIVE = auto()
    NOT_ACTIVE = auto()


class MergePolicy(Enum):
    REGULAR = auto()


class SuggestPolicy(Enum):
    REGULAR = auto()


# вся киллер фича - тут
class ScheduleBase(BaseModel):
    # TODO: truthy BASE
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    status: Optional[ScheduleStatus] = Field(default=ScheduleStatus.NOT_ACTIVE)
    # TODO: change for another data struct?
    valid_from: Optional[date] = Field(default=date.today())
    # Здесь нужно не valid_to а valid_for в количестве дней, либо месяцев, либо часов!!!
    valid_for_days: Optional[timedelta] = Field(default=timedelta(days=30))
    # TODO: array of masks?
    mask_weekdays: Optional[DaysOfWeek] = Field(default=DaysOfWeek.ALL)
    mask_weeks: Optional[WeeksInYear] = Field(default=WeeksInYear.ALL)
    mask_quartals: Optional[Quartals] = Field(default=Quartals.ALL)
    mask_days_month: Optional[DaysInMonth] = Field(default=None)
    # TODO: array of nth weekdays index?
    nth_weekday: Optional[DaysOfWeek] = Field(default=0)
    nth_index: Optional[int] = Field(None, ge=1, le=31)
    # TODO: change for another data struct?
    slot_type: Optional[SlotType] = Field(default=SlotType.ACCESSIBLE)
    slot_min_time: Optional[int] = Field(None, ge=1, le=1440)
    slot_max_time: Optional[int] = Field(None, ge=1, le=1440)
    slot_step_time: Optional[int] = Field(None, ge=1, le=1440)
    # TODO: change for another data struct?
    hour_start: Optional[int] = Field(None, ge=0, le=24)
    hour_end: Optional[int] = Field(None, ge=0, le=24)
    # TODO: policy array?
    policy_merge: Optional[str] = Field(default=MergePolicy.REGULAR)
    policy_suggest: Optional[str] = Field(default=SuggestPolicy.REGULAR)

    rental_id: Optional[int] = Field(None)

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class ScheduleCreate(ScheduleBase):
    ...


class ScheduleGet(ScheduleBase):
    id: int
