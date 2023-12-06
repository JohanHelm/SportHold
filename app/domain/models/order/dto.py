from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import DateTime


class OrderBase(BaseModel):

    customer_id: int
    full_name: str
    tarif: int
    date_time: DateTime
    duration: int
    active: int = Field(default=1)
    prolong: int = Field(default=1)

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class OrderCreate(OrderBase):
    ...


class OrderGet(OrderBase):
    order_id: int
