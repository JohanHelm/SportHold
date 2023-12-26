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

    created_at: Mapped[DateTime] = mapped_column(DateTime)

    user: Mapped["User"] = relationship(back_populates="records")
    slot: Mapped["Slot"] = relationship(back_populates="records")
    rental: Mapped["Rental"] = relationship(back_populates="records")

    __table_args__ = (UniqueConstraint("user_id", "slot_id"),)