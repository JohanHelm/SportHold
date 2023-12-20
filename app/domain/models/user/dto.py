from datetime import datetime
from enum import IntFlag, IntEnum
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
    id: int  # telegram account id here!!
    username: str
    fullname: str
    created_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = Field(default=False)
    roles: UserRole = Field(default=UserRole.REGULAR)
    subsription_type: SubscrptionType = Field(default=SubscrptionType.REGULAR)

    model_config = ConfigDict(from_attributes=True)
    # TODO: records: List[Record] =
