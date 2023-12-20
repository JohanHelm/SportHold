import datetime
from pydantic import BaseModel, ConfigDict


class RecordBase(BaseModel):
    user_id: int
    slot_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class RecordCreate(RecordBase):
    ...


class RecordGet(RecordBase):
    id: int
