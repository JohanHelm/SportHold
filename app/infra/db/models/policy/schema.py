from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from ...models import Base

if TYPE_CHECKING:
    from ..user.schema import User
    from ..slot.schema import Slot
    from ..rental.schema import Rental


class Policy(Base):
    __tablename__ = "polices"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    rental_id: Mapped[int] = mapped_column(ForeignKey("rentals.id"), unique=False)
    rental: Mapped[Rental] = relationship(back_populates="policy")
    created: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now())
    book_limit_days: Mapped[int] = mapped_column(Integer)
    need_user_phone: Mapped[bool] = mapped_column(Boolean)
    need_confirm: Mapped[bool] = mapped_column(Boolean)

    def __str__(self):
        return (
            f"SQLA Polocy,"
            f"id: {self.id},"
            f"rental_id: {self.rental_id},"
            f"created: {self.created},"
            f"book_limit_days: {self.book_limit_days}, "
            f"need_user_phone: {self.need_user_phone}, "
            f"need_confirm: {self.need_confirm}, "
        )
