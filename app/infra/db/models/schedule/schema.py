from typing import TYPE_CHECKING, List

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.types import JSON

from ...models import Base

if TYPE_CHECKING:
    from rental.schema import Rental
    from slot.schema import Slot


class Schedule(Base):
    __tablename__ = "schedules"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(
        String
    )  # TODO: вынести статусы в отдельный перечень
    conditions: Mapped[JSON] = mapped_column(
        JSON, nullable=True
    )  # TODO: описание условий для генерации слотов, необходимо продумать схему
    rental_id: Mapped[int] = mapped_column(ForeignKey("rentals.id"))
    rental: Mapped["Rental"] = relationship(back_populates="schedules")
    slots: Mapped[List["Slot"]] = relationship()

    def __str__(self):
        return (
            f"SQLA Schedule,"
            f" id: {self.id},"
            f" description: {self.description},"
            f" rental: {self.rental.id},"
            f" slots count: {len(self.slots)},"
            f" status: {self.status},"
            f" conditions: {self.conditions}"
        )
