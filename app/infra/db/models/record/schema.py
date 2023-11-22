from typing import TYPE_CHECKING
from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

# from ..user.schema import User
# from ..slot.schema import Slot

# from ...models import Base
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# if TYPE_CHECKING:
#     ..user.schema import User
#     ..slot.schema import Slot


class Record(Base):
    __tablename__ = "records"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=False)
    slot_id: Mapped[int] = mapped_column(ForeignKey("slots.id"), unique=False)
    user: Mapped["User"] = relationship(back_populates="records")
    slot: Mapped["Slot"] = relationship(back_populates="record")

    __table_args__ = (UniqueConstraint("user_id", "slot_id"),)

    def __str__(self):
        return f"SQLA Record, id: {self.id}, user: {self.user.id}, slot: {self.slot.id}"
