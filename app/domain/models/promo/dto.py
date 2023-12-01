from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import DateTime


class PromoBase(BaseModel):

    promo_code: str
    active: int = Field(default=1)
    promo_money: int
    used_times: int = Field(default=0)
    expires_at: DateTime
    times_to_use: int

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class PromoCreate(PromoBase):
    ...


class PromoGet(PromoBase):
    ...
