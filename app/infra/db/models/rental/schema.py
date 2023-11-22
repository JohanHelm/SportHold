from typing import List, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

# from ..schedule.schema import Schedule

# from ...models import Base
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# if TYPE_CHECKING:
#     ..schedule.schema import Schedule


class Rental(Base):
    __tablename__ = "rentals"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    schedules: Mapped[List["Schedule"]] = relationship()

    def __str__(self):
        return f"SQLA Rental," \
               f" id: {self.id}," \
               f" type: {self.type}," \
               f" name: {self.name}," \
               f" description: {self.description}," \
               f" schedules count: {len(self.schedules)}"
