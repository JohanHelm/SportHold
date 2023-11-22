from typing import TYPE_CHECKING, List

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.types import JSON

# from ..slot.schema import Slot
# from ..rental.schema import Rental

# from ...models import Base
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# if TYPE_CHECKING:
#     from ..slot.schema import Slot
#     from ..rental.schema import Rental


# class Schedule(Base):
#     __tablename__ = "schedule"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String)
#     desc: Mapped[str] = mapped_column(String)
#     days_open: Mapped[str] = mapped_column(ARRAY(Integer))
#     open_from: Mapped[time] = mapped_column(Time)
#     open_until: Mapped[time] = mapped_column(Time)
#     min_book_time: Mapped[timedelta] = mapped_column(Interval)
#     max_book_time: Mapped[timedelta] = mapped_column(Interval)
#     time_step: Mapped[timedelta] = mapped_column(Interval)
#     slot: Mapped[List["Slot"]] = relationship(back_populates="schedule")

class Schedule(Base):
    __tablename__ = "schedules"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(
        String
    )  # TODO: вынести статусы в отдельный перечень
    conditions: Mapped[str] = mapped_column(String)
    # conditions: Mapped[JSON] = mapped_column(
    #     JSON, nullable=True, arbitrary_types_allowed=True
    # )  # TODO: описание условий для генерации слотов, необходимо продумать схему
    rental_id: Mapped[int] = mapped_column(ForeignKey("rentals.id"))
    rental: Mapped["Rental"] = relationship(back_populates="schedules")
    slots: Mapped[List["Slot"]] = relationship()

    def __str__(self):
        return f"SQLA Schedule," \
               f" id: {self.id}," \
               f" description: {self.description}," \
               f" rental: {self.rental.id}," \
               f" slots count: {len(self.slots)}," \
               f" status: {self.status}," \
               f" conditions: {self.conditions}"
