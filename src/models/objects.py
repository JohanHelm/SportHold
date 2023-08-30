from pydantic import Field
from uuid import UUID, uuid4

from pydantic import BaseModel
from typing import List


class BaseObject(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str = None
    desc: str = None
    schedules: List[UUID] = None
