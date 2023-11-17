from datetime import date, datetime
from enum import Enum
from typing import List
from sqlalchemy import (
    DateTime,
    UniqueConstraint,
    create_engine,
    Integer,
    String,
    ForeignKey
)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm import Mapped, declarative_base
from sqlalchemy.orm import mapped_column
from sqlalchemy.types import JSON
from pydantic import BaseModel


class WorkDays(str, Enum):
    monday = "MONDAY"
    tuesday = "TUESDAY"
    wednesday = "WEDNESDAY"
    thursday = "THURSDAY"
    friday = "FRIDAY"
    saturday = "SATURDAY"
    sunday = "SUNDAY"


class ExeptionType(str, Enum):
    access = "ACCESS"
    forbidden = "FORBIDDEN"


class ConditionType(str, Enum):
    flex_slot = "FLEX_SLOT"
    solid_slot = "SOLID_SLOT"
    manual_slot = "MANUAL_SLOT"


class ConditionExeption(BaseModel):
    type: ExeptionType
    day: date
    start_hour: int
    end_hour: int


class Conditions(BaseModel):
    type: ConditionType
    start_at: datetime
    end_at: datetime
    work_days: List[WorkDays]
    exceptions: List[ConditionExeption]
    start_hour: int
    end_hour: int
    min_time: int
    max_time: int
    book_range_hours: int


Base = declarative_base()
engine = create_engine("sqlite:///example.db", echo=False)
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(String)
    username: Mapped[str] = mapped_column(String)
    records: Mapped[List["Record"]] = relationship()

    def __str__(self):
        return f"SQLA User, id: {self.id}, TG id: {self.tg_id}, username: {self.username}, active records count: {len(self.records)}"


class Rental(Base):
    __tablename__ = "rentals"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    schedules: Mapped[List["Schedule"]] = relationship()

    def __str__(self):
        return f"SQLA Rental, id: {self.id}, type: {self.type}, name: {self.name}, description: {self.description}, schedules count: {len(self.schedules)}"


class Schedule(Base):
    __tablename__ = "schedules"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(
        String
    )  # TODO: вынести статусы в отдельный перечень
    conditions: Mapped[JSON] = mapped_column(
        JSON, nullable=True
    )  # TODO: описание условий для генерации слотов, необходимо продумать схему
    rental_id: Mapped[int] = mapped_column(ForeignKey("rentals.id"))
    rental: Mapped[Rental] = relationship(back_populates="schedules")
    slots: Mapped[List["Slot"]] = relationship()

    def __str__(self):
        return f"SQLA Schedule, id: {self.id}, description: {self.description}, rental: {self.rental.id}, slots count: {len(self.slots)}, status: {self.status}, conditions: {self.conditions}"


class Slot(Base):
    __tablename__ = "slots"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    started_at: Mapped[DateTime] = mapped_column(DateTime)
    duration: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(
        String
    )  # TODO: вынести статусы в отдельный перечень
    schedule_id: Mapped[int] = mapped_column(ForeignKey("schedules.id"))
    record: Mapped[List["Record"]] = relationship()
    schedule: Mapped["Schedule"] = relationship(back_populates="slots")

    def __str__(self):
        return f"SQLA Slot, id: {self.id}, schedule: {self.schedule.id}, records: {[str(x) for x in self.record]}, start at: {self.started_at}, duration: {self.duration}, status: {self.status}"


class Record(Base):
    __tablename__ = "records"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=False)
    slot_id: Mapped[int] = mapped_column(ForeignKey("slots.id"), unique=False)
    user: Mapped[User] = relationship(back_populates="records")
    slot: Mapped[Slot] = relationship(back_populates="record")

    __table_args__ = (UniqueConstraint("user_id", "slot_id"),)

    def __str__(self):
        return f"SQLA Record, id: {self.id}, user: {self.user.id}, slot: {self.slot.id}"


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

user = User(tg_id=103273, username="@telegram_test_user")
user_2 = User(tg_id=103272, username="@telegram_test_user_2")
rental = Rental(
    name="Ping-pong table",
    description="Free-to-play ping-pong table on 2nd floor",
    type="SPORT",
)

session.add_all([user, rental, user_2])
session.commit()
print(user, rental, sep="\n")

schedule = Schedule(
    description="Basic schedule for pin-pong table",
    status="ACTIVE",
    conditions={"key": "value"},
)
schedule.rental = rental
session.add_all([schedule])
session.commit()
print(schedule)


slot = Slot(started_at=datetime(2023, 12, 1, 12, 12), duration=30, status="PLANNED")
schedule.slots.append(slot)

session.commit()
print(slot)

record = Record()
record.slot = slot
record.user = user
session.add(record)
session.commit()

print(record)
print(slot)

existing_slot = session.get(Slot, 1)
record_2 = Record(slot_id=existing_slot.id)
record_2.user = user_2
session.add(record_2)
session.commit()

print(slot)
