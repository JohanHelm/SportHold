from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from ...models import Base

if TYPE_CHECKING:
    from ..record.schema import Record
    from ..schedule.schema import Schedule
    from ..rental.schema import Rental


class Slot(Base):
    __tablename__ = "slots"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    rental_id: Mapped[int] = mapped_column(ForeignKey("rentals.id"))
    schedule_id: Mapped[int] = mapped_column(ForeignKey("schedules.id"))

    started_at: Mapped[DateTime] = mapped_column(DateTime)
    ended_at: Mapped[DateTime] = mapped_column(DateTime)
    status: Mapped[int] = mapped_column(default=0)
    type: Mapped[int] = mapped_column(default=0)

    records: Mapped[Optional[List["Record"]]] = relationship(back_populates="slot")
    schedule: Mapped["Schedule"] = relationship(back_populates="slots")
    rental: Mapped["Rental"] = relationship(back_populates="slots")

    def __str__(self):
        return (
            f"SQLA Slot, "
            f"id: {self.id},"
            f" schedule: {self.schedule_id},"
            f" started_at at: {self.started_at},"
            f" ended_at: {self.ended_at},"
            f" status: {self.status}"
        )
