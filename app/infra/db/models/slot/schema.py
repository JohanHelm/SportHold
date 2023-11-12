from datetime import date, time, timedelta
from sqlalchemy import Integer, Date, Time, ARRAY, ForeignKey
from sqlalchemy.types import Interval
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from ...models import Base

class Slot(Base):
    __tablename__ = "slot"

    id: Mapped[int] = mapped_column(primary_key=True)
    start_date: Mapped[date] = mapped_column(Date)
    start_time: Mapped[time] = mapped_column(Time)
    timedelta: Mapped[timedelta] = mapped_column(Interval)
    user_id_deque: Mapped[str] = mapped_column(ARRAY(Integer))
    schedule_id: Mapped[int] = mapped_column(Integer, ForeignKey("schedule.id"), nullable=True)
    schedule: Mapped["Schedule"] = relationship(back_populates="slot")