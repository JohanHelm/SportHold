import logging

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from app.infra.db.sqlite.repository import Base

logger = logging.getLogger(__name__)


class User(Base):
    __tablename__ = "user"

    id : Mapped[int]= mapped_column(Integer, primary_key=True, index=True)
    fullname: Mapped[str] = mapped_column(String)
    username: Mapped[str] = mapped_column(String)
    locale: Mapped[str] = mapped_column(String, default="ru")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)