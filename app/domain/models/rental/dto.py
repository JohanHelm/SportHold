from enum import IntEnum
from optparse import Option
from typing import Optional
from pydantic import BaseModel, ConfigDict

# from app.domain.models.user.dto import UserBase


class RentalType(IntEnum):
    REGULAR = 1  # Обычный спортивный объект


class RentalBase(BaseModel):
    name: str
    description: str
    rental_type: RentalType

    model_config = ConfigDict(from_attributes=True)


class RentalCreate(RentalBase):
    ...


class RentalGet(RentalBase):
    id: int
