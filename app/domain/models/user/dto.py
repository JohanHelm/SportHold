from ast import List
from datetime import date
from enum import IntFlag, IntEnum
from typing import Optional
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
    tg_id: int
    username: str
    roles: UserRole
    subscription_type: Optional[SubscrptionType] = Field(default=None)
    subscription_valid_for: Optional[date] = Field(default=None)
    wallet_balance: int = Field(default=0)
    rentals: List[RentalBase]
    
    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    ...


class UserGet(UserBase):
    id: int
