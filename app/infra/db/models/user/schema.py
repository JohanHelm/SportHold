from typing import TYPE_CHECKING, List
from sqlalchemy import Integer, String, DateTime, ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from ...models import Base

from app.domain.models.user.dto import UserRole

if TYPE_CHECKING:
    from ..record.schema import Record

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String)
    fullname: Mapped[str] = mapped_column(String)
    lang_code: Mapped[str] = mapped_column(String)
    registration_date: Mapped[DateTime] = mapped_column(DateTime)
    active: Mapped[int] = mapped_column(Integer, default=1)
    # roles: Mapped[List["UserRole"]] = mapped_column(ARRAY(Integer), default=[1])
    records: Mapped[List["Record"]] = relationship()


    def __str__(self):
        return (
            f"SQLA User,"
            f" user_id: {self.user_id},"
            f" username: {self.username},"
            f" fullname: {self.fullname},"
            f" lang_code: {self.lang_code},"
            f" registartion date: {self.registration_date},"
            f" active: {self.active},"
            f" active records count: {len(self.records)}"
        )
