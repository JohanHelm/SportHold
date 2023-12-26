from datetime import datetime
from typing import TYPE_CHECKING, List
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from app.infra.db.models.utils.helpers import UserRole, UserStatus

from ...models import Base

if TYPE_CHECKING:
    from ..record.schema import Record


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    username: Mapped[str] = mapped_column(String)
    fullname: Mapped[str] = mapped_column(String)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now())
    status: Mapped[int] = mapped_column(Integer, default=UserStatus.ACTIVE)
    roles: Mapped[int] = mapped_column(Integer, default=UserRole.REGULAR)

    records: Mapped[List["Record"]] = relationship(back_populates="user")

    def __str__(self):
        return (
            f"SQLA User, "
            f"id: {self.id}, "
            f"username: {self.username}, "
            f"fullname: {self.fullname}, "
            f"created_at: {self.created_at}, "
            f"status: {UserStatus(self.status).custom_print()}, "
            f"roles: {UserRole(self.roles).custom_print()}"
        )
