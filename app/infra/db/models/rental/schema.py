from typing import TYPE_CHECKING, List
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from ...models import Base

if TYPE_CHECKING:
    from ..schedule.schema import Schedule


class Rental(Base):
    __tablename__ = "rentals"

    rental_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    schedules: Mapped[List["Schedule"]] = relationship()

    def __str__(self):
        return (
            f"SQLA Rental,"
            f" id: {self.rental_id},"
            f" type: {self.category},"
            f" name: {self.name},"
            f" description: {self.description},"
            f" schedules count: {len(self.schedules)}"
        )
