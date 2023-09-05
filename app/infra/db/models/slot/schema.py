from typing import Deque, Optional
from datetime import date, time, timedelta
from collections import deque

from sqlalchemy import Integer, String, Date, Time
from sqlalchemy.types import Interval
from sqlalchemy.orm import Mapped, declarative_base
from sqlalchemy.orm import mapped_column

Base = declarative_base()

class Slot(Base):
    __tablename__ = "slot"

    id: Mapped[int] = mapped_column(primary_key=True)
    schedule_id: Mapped[int] = mapped_column(Integer)
    start_date: Mapped[date]
    start_time: Mapped[time]
    timedelta: Mapped[timedelta] = mapped_column(Interval)
    user_id_deque: Mapped[str] = mapped_column(String)