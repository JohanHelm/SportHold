from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, Integer, String, ForeignKey, BIGINT
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from datetime import date

from ...models import Base

from app.helpers.maskers.weekdays import DaysOfWeek
from app.helpers.maskers.weeks import WeeksInYear
from app.helpers.maskers.quartals import Quartals
from app.helpers.maskers.daysmonth import DaysInMonth
from app.domain.models.slot.dto import SlotType
from app.domain.models.schedule.dto import SuggestPolicy, MergePolicy


if TYPE_CHECKING:
    from ..rental.schema import Rental
    from ..slot.schema import Slot


class Schedule(Base):
    __tablename__ = "schedules"

    schedule_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[int] = mapped_column(Integer, default=2)
    valid_from: Mapped[DateTime] = mapped_column(DateTime, default=date.today())
    valid_for_days: Mapped[int] = mapped_column(Integer, default=30)
    mask_weekdays: Mapped[int] = mapped_column(Integer, default=127)
    mask_weeks: Mapped[int] = mapped_column(BIGINT, default=4503599627370495)
    mask_quartals: Mapped[int] = mapped_column(Integer, default=15)
    mask_days_month: Mapped[int] = mapped_column(Integer, nullable=True)
    nth_weekday: Mapped[int] = mapped_column(Integer, nullable=True)
    nth_index: Mapped[int] = mapped_column(Integer, nullable=True)
    slot_type: Mapped[int] = mapped_column(Integer, default=1)
    slot_min_time: Mapped[int] = mapped_column(Integer, nullable=True)
    slot_max_time: Mapped[int] = mapped_column(Integer, nullable=True)
    slot_step_time: Mapped[int] = mapped_column(Integer, nullable=True)
    hour_start: Mapped[int] = mapped_column(Integer, nullable=True)
    hour_end: Mapped[int] = mapped_column(Integer, nullable=True)
    policy_merge: Mapped[int] = mapped_column(Integer, default=1)
    policy_suggest: Mapped[int] = mapped_column(Integer, default=1)
    rental_id: Mapped[int] = mapped_column(ForeignKey("rentals.rental_id"))
    rental: Mapped["Rental"] = relationship(back_populates="schedules")
    slots: Mapped[List["Slot"]] = relationship()

    def __str__(self):
        return (
            f"SQLA Schedule,"
            f" id: {self.schedule_id},"
            f" name: {self.name},"
            f" description: {self.description},"
            f" status: {self.status},"
            f" valid_from: {self.valid_from},"
            f" valid_for_days: {self.valid_for_days},"
            f" mask_weekdays: {DaysOfWeek(self.mask_weekdays)},"
            f" mask_weeks: {WeeksInYear(self.mask_weeks)},"
            f" mask_quartals: {Quartals(self.mask_quartals)},"
            f" mask_days_month: {DaysInMonth(self.mask_days_month)},"
            f" nth_weekday: {DaysOfWeek(self.nth_weekday)},"
            f" nth_index: {self.nth_index},"
            f" slot_type: {SlotType(self.slot_type)},"
            f" slot_min_time: {self.slot_min_time},"
            f" slot_max_time: {self.slot_max_time},"
            f" slot_step_time: {self.slot_step_time},"
            f" hour_start: {self.hour_start},"
            f" hour_end: {self.hour_end},"
            f" policy_merge: {MergePolicy(self.policy_merge)},"
            f" policy_suggest: {SuggestPolicy(self.policy_suggest)},"
            f" rental: {self.rental.rental_id},"
            f" slots count: {len(self.slots)},"
        )
