from pydantic import BaseModel, ConfigDict
from sqlalchemy import DateTime
from enum import Enum, auto


class PaymentMethod(Enum):
    CRYPTA = auto()
    QIWI = auto()
    YOOMONEY = auto()
    CARD = auto()


class IncomeBase(BaseModel):

    customer_id: int
    full_name: str
    summ: int
    date_time: DateTime
    method: PaymentMethod

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class IncomeCreate(IncomeBase):
    ...


class IncomeGet(IncomeBase):
    income_id: int
