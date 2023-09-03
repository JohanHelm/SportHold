import logging
from typing import Optional

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from app.infra.db.sqlite.repository import Base

logger = logging.getLogger(__name__)


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(Integer)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[Optional[str]]
    username: Mapped[Optional[str]]
    language_code: Mapped[Optional[str]]
    is_premium: Mapped[Optional[bool]]
    is_bot: Mapped[Optional[bool]]

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.username!r})"