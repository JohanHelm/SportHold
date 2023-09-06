from pydantic import BaseModel, ConfigDict


class ObjectBase(BaseModel):
    name: str = None
    desc: str = None

    model_config = ConfigDict(from_attributes=True)


class ObjectCreate(ObjectBase):
    ...


class ObjectGet(ObjectBase):
    id: int
