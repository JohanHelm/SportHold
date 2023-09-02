from uuid import UUID, uuid4
from pydantic import BaseModel, Field

class BaseUser(BaseModel):
    id: int
    fullname: str
    username: str
    locale: str


    class Config:
        orm_mode = True