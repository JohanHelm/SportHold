from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import Enum, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from app.infra.db.models.utils.helpers import SlotStatus, SlotType

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

    created: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now())

    started: Mapped[DateTime] = mapped_column(DateTime)
    ended: Mapped[DateTime] = mapped_column(DateTime)
    status: Mapped[int] = mapped_column(Integer, default=SlotStatus.INACTIVE)
    type: Mapped[int] = mapped_column(Integer, default=SlotType.ACCESSIBLE)

    records: Mapped[Optional[List["Record"]]] = relationship(back_populates="slot")
    schedule: Mapped["Schedule"] = relationship(back_populates="slots")
    rental: Mapped["Rental"] = relationship(back_populates="slots")

    def __str__(self):
        return (
            f"SQLA Slot, "
            f"id: {self.id}, "
            f"status: {SlotStatus(self.status).custom_print()} "
            f"type: {SlotType(self.type).custom_print()} "
            f"created: {self.created}, "
            f"schedule id: {self.schedule_id}, "
            f"started: {self.started}, "
            f"ended: {self.ended}"
        )
