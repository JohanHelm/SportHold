from pydantic import BaseModel


class BaseUser(BaseModel):
    fname: str
    lname: str
    tg_id: int
