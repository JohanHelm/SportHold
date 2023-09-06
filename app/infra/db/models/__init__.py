from sqlalchemy.orm import declarative_base

Base = declarative_base()

from .user.schema import User
from .schedule.schema import Schedule
from .slot.schema import Slot
from .object.schema import Object