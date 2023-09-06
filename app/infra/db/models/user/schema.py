from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, declarative_base
from sqlalchemy.orm import mapped_column

from ...models import Base

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
