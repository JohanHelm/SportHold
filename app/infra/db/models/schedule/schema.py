from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from datetime import date, datetime, timedelta

from app.domain.helpers.enums import ScheduleStatus, SlotType, DaysOfWeek

from ...models import Base


if TYPE_CHECKING:
    from ..rental.schema import Rental
    from ..slot.schema import Slot


class Schedule(Base):
    __tablename__ = "schedules"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    rental_id: Mapped[int] = mapped_column(ForeignKey("rentals.id"))

    mask_days: Mapped[int] = mapped_column(Integer, default=DaysOfWeek.ALL)

    name: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[int] = mapped_column(Integer, default=ScheduleStatus.INACTIVE)
    started: Mapped[DateTime] = mapped_column(DateTime, default=date.today())
    ended: Mapped[DateTime] = mapped_column(
        Integer, default=date.today() + timedelta(days=30)
    )
    created: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now())
    slot_type: Mapped[int] = mapped_column(Integer, default=SlotType.ACCESSIBLE)
    slot_time: Mapped[int] = mapped_column(Integer, default=30)
    hour_start: Mapped[int] = mapped_column(Integer, default=9)
    hour_end: Mapped[int] = mapped_column(Integer, default=18)

    rental: Mapped["Rental"] = relationship(back_populates="schedules")
    slots: Mapped[List["Slot"]] = relationship(back_populates="schedule")

    # TODO допилить текстовое представление экземпляра, сейчас падает с ошибкой на полях где есть None
    def __str__(self):
        return (
            f"SQLA Schedule, "
            f"id: {self.id}, "
            f"name: {self.name}, "
            f"description: {self.description}, "
            f"status: {ScheduleStatus(self.status).custom_print()}, "
            f"created: {self.created}, "
            f"started: {self.started}, "
            f"ended: {self.ended}, "
            f"weekdays: {DaysOfWeek(self.mask_days).custom_print()}, "
            f"slot_type: {SlotType(self.slot_type).custom_print()}, "
            f"slot_time: {self.slot_time}, "
            f"hour_start: {self.hour_start}, "
            f"hour_end: {self.hour_end}, "
            f"rental_id: {self.rental_id}"
        )
