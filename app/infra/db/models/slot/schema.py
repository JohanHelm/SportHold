from typing import TYPE_CHECKING, List
from sqlalchemy import Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from ...models import Base

if TYPE_CHECKING:
    from ..record.schema import Record
    from ..schedule.schema import Schedule


class Slot(Base):
    __tablename__ = "slots"

    slot_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    started_at: Mapped[DateTime] = mapped_column(DateTime)
    ended_at: Mapped[DateTime] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(
        String
    )  # TODO: вынести статусы в отдельный перечень
    type: Mapped[str] = mapped_column(String)
    schedule_id: Mapped[int] = mapped_column(ForeignKey("schedules.schedule_id"))
    record: Mapped[List["Record"]] = relationship()
    schedule: Mapped["Schedule"] = relationship(back_populates="slots")

    # def __str__(self):
    #     return (
    #         f"SQLA Slot, "
    #         f"id: {self.slot_id},"
    #         f" schedule: {self.schedule.schedule_id},"
    #         f" records: {[str(x) for x in self.record]},"
    #         f" start at: {self.started_at},"
    #         f" duration: {self.duration},"
    #         f" status: {self.status}"
    #     )
