from typing import TYPE_CHECKING
from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from ...models import Base

if TYPE_CHECKING:
    from ..user.schema import User
    from ..slot.schema import Slot

class Record(Base):
    __tablename__ = "records"

    record_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), unique=False)
    slot_id: Mapped[int] = mapped_column(ForeignKey("slots.slot_id"), unique=False)
    user: Mapped["User"] = relationship(back_populates="records")
    slot: Mapped["Slot"] = relationship(back_populates="record")

    __table_args__ = (UniqueConstraint("user_id", "slot_id"),)

    def __str__(self):
        return f"SQLA Record, id: {self.record_id}, user: {self.user.user_id}, slot: {self.slot.slot_id}"
