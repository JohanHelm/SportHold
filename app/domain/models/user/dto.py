from pydantic import BaseModel, ConfigDict
from typing import Optional


class UserBase(BaseModel):
    tg_id: int
    first_name: Optional[str]
    last_name: Optional[str]
    username: str
    language_code: Optional[str]
    is_premium: Optional[bool]
    is_bot: Optional[bool]

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    ...


class UserGet(UserBase):
    id: int
