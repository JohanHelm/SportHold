from datetime import date, time, timedelta
from sqlalchemy import Integer, String, Date, Time, ARRAY
from sqlalchemy.types import Interval
from sqlalchemy.orm import Mapped, declarative_base
from sqlalchemy.orm import mapped_column

Base = declarative_base()

class Slot(Base):
    __tablename__ = "slot"

    id: Mapped[int] = mapped_column(primary_key=True)
    schedule_id: Mapped[int] = mapped_column(Integer)
    start_date: Mapped[date] = mapped_column(Date)
    start_time: Mapped[time] = mapped_column(Time)
    timedelta: Mapped[timedelta] = mapped_column(Interval)
    user_id_deque: Mapped[str] = mapped_column(ARRAY(Integer))

#TODO https://docs.sqlalchemy.org/en/14/core/type_basics.html#sqlalchemy.types.ARRAY -> user_id_deque: Mapped[str] = mapped_column(String)