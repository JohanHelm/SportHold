from datetime import datetime
from typing import TYPE_CHECKING, List
from sqlalchemy import Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

# from ..record.schema import Record
# from ..schedule.schema import Schedule

# from ...models import Base
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# if TYPE_CHECKING:
#     from ..record.schema import Record
#     from ..schedule.schema import Schedule


# class Slot(Base):
#     __tablename__ = "slot"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     start_date: Mapped[date] = mapped_column(Date)
#     start_time: Mapped[time] = mapped_column(Time)
#     timedelta: Mapped[timedelta] = mapped_column(Interval)
#     user_id_deque: Mapped[str] = mapped_column(ARRAY(Integer))
#     schedule_id: Mapped[int] = mapped_column(
#         Integer, ForeignKey("schedule.id"), nullable=True
#     )
#     schedule: Mapped["Schedule"] = relationship(back_populates="slot")


class Slot(Base):
    __tablename__ = "slots"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    started_at: Mapped[datetime] = mapped_column(datetime)
    # started_at: Mapped[DateTime] = mapped_column(DateTime)
    duration: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(
        String
    )  # TODO: вынести статусы в отдельный перечень
    schedule_id: Mapped[int] = mapped_column(ForeignKey("schedules.id"))
    record: Mapped[List["Record"]] = relationship()
    schedule: Mapped["Schedule"] = relationship(back_populates="slots")

    def __str__(self):
        return f"SQLA Slot, " \
               f"id: {self.id}," \
               f" schedule: {self.schedule.id}," \
               f" records: {[str(x) for x in self.record]}," \
               f" start at: {self.started_at}," \
               f" duration: {self.duration}," \
               f" status: {self.status}"
