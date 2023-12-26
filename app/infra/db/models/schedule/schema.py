from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, Enum, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from datetime import date, timedelta

from app.infra.db.models.utils.helpers import ScheduleStatus, SlotType

from ...models import Base



if TYPE_CHECKING:
    from ..rental.schema import Rental
    from ..slot.schema import Slot


class Schedule(Base):
    __tablename__ = "schedules"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    rental_id: Mapped[int] = mapped_column(ForeignKey("rentals.id"))

    name: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[Enum] = mapped_column(ScheduleStatus, default=ScheduleStatus.INACTIVE)
    started_at: Mapped[DateTime] = mapped_column(DateTime, default=date.today())
    ended_at: Mapped[DateTime] = mapped_column(
        Integer, default=date.today() + timedelta(days=30)
    )
    slot_type: Mapped[Enum] = mapped_column(SlotType, default=SlotType.ACCESSIBLE)
    slot_time: Mapped[int] = mapped_column(Integer, default=30)
    hour_start: Mapped[int] = mapped_column(Integer, default=9)
    hour_end: Mapped[int] = mapped_column(Integer, default=18)

    rental: Mapped["Rental"] = relationship(back_populates="schedules")
    slots: Mapped[List["Slot"]] = relationship(back_populates="schedule")

    # TODO допилить текстовое представление экземпляра, сейчас падает с ошибкой на полях где есть None
    def __str__(self):
        return (
            f"SQLA Schedule,"
            f" id: {self.id},"
            f" name: {self.name},"
            f" description: {self.description},"
            f" status: {self.status},"
            f" started_at: {self.started_at},"
            f" ended_at: {self.ended_at},"
            f" slot_type: {self.slot_type},"
            f" slot_time: {self.slot_time},"
            f" hour_start: {self.hour_start},"
            f" hour_end: {self.hour_end},"
            f" rental_id: {self.rental.rental_id}"
        )
