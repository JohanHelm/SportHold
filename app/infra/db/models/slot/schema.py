from datetime import date, time, timedelta
from sqlalchemy import Integer, String
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

#TODO https://docs.sqlalchemy.org/en/14/core/type_basics.html#sqlalchemy.types.ARRAY -> user_id_deque: Mapped[str] = mapped_column(String)