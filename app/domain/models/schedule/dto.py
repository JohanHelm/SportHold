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
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    status: Optional[ScheduleStatus] = Field(default=ScheduleStatus.NOT_ACTIVE)
    started_at: Optional[date] = Field(default=date.today())
    ended_at: Optional[date] = Field(default=date.today() + timedelta(days=30))
    slot_type: Optional[SlotType] = Field(default=SlotType.ACCESSIBLE)
    slot_min_time: Optional[int] = Field(None, ge=1, le=1440)
    slot_max_time: Optional[int] = Field(None, ge=1, le=1440)
    slot_step_time: Optional[int] = Field(None, ge=1, le=1440)
    hour_start: Optional[int] = Field(None, ge=0, le=24)
    hour_end: Optional[int] = Field(None, ge=0, le=24)
    policy_merge: Optional[str] = Field(default=MergePolicy.REGULAR)
    policy_suggest: Optional[str] = Field(default=SuggestPolicy.REGULAR)

    rental_id: Optional[int] = Field(None)

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    def __hash__(self) -> int:  # change to FROZEN pydantic
        return self.name.__hash__()  # or self.id.__hash__()


class ScheduleCreate(ScheduleBase):
    ...


class ScheduleGet(ScheduleBase):
    id: int
