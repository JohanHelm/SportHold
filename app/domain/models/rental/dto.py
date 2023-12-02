from enum import IntEnum
from optparse import Option
from typing import Optional
from pydantic import BaseModel, ConfigDict
# from app.domain.models.user.dto import UserBase


class RentalType(IntEnum):
    REGULAR = 1


class RentalBase(BaseModel):
    name: str
    description: str
    rental_type: RentalType
    user_id: int #Optional[UserBase]

    model_config = ConfigDict(from_attributes=True)


class RentalCreate(RentalBase):
    ...


class RentalGet(RentalBase):
    rental_id: int
