from typing import TYPE_CHECKING, List
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from ...models import Base

if TYPE_CHECKING:
    from ..record.schema import Record

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(Integer)
    username: Mapped[str] = mapped_column(String)
    records: Mapped[List["Record"]] = relationship()

    def __str__(self):
        return (
            f"SQLA User,"
            f" id: {self.id},"
            f" TG id: {self.tg_id},"
            f" username: {self.username},"
            f" active records count: {len(self.records)}"
        )
