from typing import TYPE_CHECKING, List
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.infra.db.models.utils.helpers import RentalTypes

from ...models import Base

if TYPE_CHECKING:
    from ..schedule.schema import Schedule
    from ..slot.schema import Slot
    from ..record.schema import Record


class Rental(Base):
    _tablename__ = "rentals"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    type: Mapped[int] = mapped_column(Integer, default=RentalTypes.REGULAR)

    schedules: Mapped[List["Schedule"]] = relationship(back_populates="rental")
    slots: Mapped[List["Slot"]] = relationship(back_populates="rental")
    records: Mapped[List["Record"]] = relationship(back_populates="rental")

    def __str__(self):
        return (
            f"SQLA Rental, "
            f"id: {self.id}, "
            f"category: {RentalTypes(self.type).custom_print()}, "
            f"name: {self.name}, "
            f"description: {self.description} "
            f"schedules: {len(self.schedules)} "
            f"slots: {len(self.slots)} "
            f"records: {len(self.records)}"
        )
