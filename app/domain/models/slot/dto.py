from enum import Enum
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class SlotType(Enum):
    ACCESSIBLE = 1
    RESTRICTED = 2


class SlotStatus(Enum):
    FREE = 1
    READY = 2
    VALID = 3
    DONE = 4
    UNDONE = 5


class SlotBase(BaseModel):
    started_at: datetime
    # TODO:  ended_at: datetime
    status: SlotStatus
    type: SlotType
    # TODO: records: Optional[List[Record]]
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class SlotCreate(SlotBase):
    ...


class SlotGet(SlotBase):
    id: int
    schedule_id: int
