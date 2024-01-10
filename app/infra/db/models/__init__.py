from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from .user.schema import User
from .schedule.schema import Schedule
from .slot.schema import Slot
from .rental.schema import Rental
from .record.schema import Record
from .policy.schema import Policy
