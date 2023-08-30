from uuid import UUID, uuid4
from pydantic import BaseModel, Field

class BaseUser(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    fname: str
    lname: str
    tg_id: int
