import logging

from sqlalchemy import BigInteger, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from src.db.connect import Base

logger = logging.getLogger(__name__)


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)  # <- ID telegram user

    fullname: Mapped[str] = mapped_column(VARCHAR(129), nullable=True)
    username: Mapped[str] = mapped_column(VARCHAR(32), nullable=True)
    locale: Mapped[str] = mapped_column(VARCHAR(2), default="ru")

    @property
    def to_dict(self) -> dict:
        # Converting model in dictionary
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
