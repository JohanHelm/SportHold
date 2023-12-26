from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from ...models import Base

if TYPE_CHECKING:
    from ..user.schema import User
    from ..slot.schema import Slot
    from ..rental.schema import Rental


class Record(Base):
    __tablename__ = "records"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=False)
    slot_id: Mapped[int] = mapped_column(ForeignKey("slots.id"), unique=False)
    rental_id: Mapped[int] = mapped_column(ForeignKey("rentals.id"), unique=False)
    created: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now())

    user: Mapped["User"] = relationship(back_populates="records")
    slot: Mapped["Slot"] = relationship(back_populates="records")
    rental: Mapped["Rental"] = relationship(back_populates="records")

    __table_args__ = (UniqueConstraint("user_id", "slot_id"),)

    def __str__(self):
        return (
            f"SQLA Record,"
            f"id: {self.id},"
            f"user_id: {self.user_id},"
            f"slot_id: {self.slot_id},"
            f"rental_id: {self.rental_id}, "
            f"created: {self.created}"
        )
