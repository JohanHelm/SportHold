# from ast import List
from datetime import datetime
from enum import IntFlag, IntEnum
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field

from app.domain.models.rental.dto import RentalBase


class UserRole(IntFlag):
    REGULAR = 1
    PARTNER = 2
    ADMIN = 4
    MANAGER = 8
    EMPLOYEE = 16
    OWNER = 32
    WORKER = 64
    PAID = 128


class SubscrptionType(IntEnum):
    REGULAR = 1


class UserBase(BaseModel):
    user_id: int  # telegram account id here!!
    username: str
    fullname: str
    lang_code: str
    registration_date: datetime
    active: int = Field(default=1)
    # TODO Разобраться с ролями, ренталами
    # roles: List[UserRole]
    # subscription_type: Optional[SubscrptionType] = Field(default=None)
    # subscription_valid_for: Optional[date] = Field(default=None)
    # wallet_balance: int = Field(default=0)
    # rentals: List[RentalBase]


    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    ...


class UserGet(UserBase):
    ...
