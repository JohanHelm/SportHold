from enum import Enum, auto
from pydantic import BaseModel, ConfigDict
from sqlalchemy import DateTime


class SlotType(Enum):
    ACCESSIBLE = auto()
    RESTRICTED = auto()

class SlotStatus(Enum):
    GENERATED = auto()
    
class SlotBase(BaseModel):
    started_at: DateTime
    duration: int
    status: SlotStatus
    type: SlotType
    
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class SlotCreate(SlotBase):
    ...


class SlotGet(SlotBase):
    slot_id: int
    schedule_id: int
