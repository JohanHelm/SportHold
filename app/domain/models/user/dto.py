from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    tg_id: int
    first_name: Optional[str]
    last_name: Optional[str]
    username: str
    language_code: Optional[str]
    is_premium: Optional[bool]
    is_bot: Optional[bool]

    class Config:
        orm_mode = True
        from_attributes = True


class UserCreate(UserBase):
    ...

class UserGet(UserBase):
    id: int