from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    tg_id: int
    username: str

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    ...


class UserGet(UserBase):
    id: int
