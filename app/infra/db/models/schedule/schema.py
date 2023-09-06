from datetime import time, timedelta
from sqlalchemy import Integer, String, Time, ARRAY
from sqlalchemy.types import Interval
from sqlalchemy.orm import Mapped, declarative_base
from sqlalchemy.orm import mapped_column

Base = declarative_base()

class Schedule(Base):
    __tablename__ = "schedule"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    desc: Mapped[str] = mapped_column(String)
    days_open: Mapped[str] = mapped_column(ARRAY(Integer))
    open_from: Mapped[time] = mapped_column(Time)
    open_until: Mapped[time] = mapped_column(Time)
    min_book_time: Mapped[timedelta] = mapped_column(Interval)
    max_book_time: Mapped[timedelta] = mapped_column(Interval)
    time_step: Mapped[timedelta] = mapped_column(Interval)