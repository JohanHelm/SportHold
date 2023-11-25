import asyncio
from datetime import date, datetime
from typing import List

from sqlalchemy import (
    DateTime,
    UniqueConstraint,
    Integer,
    String,
    ForeignKey,
    BIGINT
)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(Integer)
    username: Mapped[str] = mapped_column(String)
    records: Mapped[List["Record"]] = relationship()

    def __str__(self):
        return f"SQLA User, id: {self.id}, TG id: {self.tg_id}, username: {self.username}, active records count: {len(self.records)}"


class Rental(Base):
    __tablename__ = "rentals"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    schedules: Mapped[List["Schedule"]] = relationship()

    def __str__(self):
        return f"SQLA Rental, id: {self.id}, category: {self.category}, name: {self.name}, description: {self.description}, schedules count: {len(self.schedules)}"


class Schedule(Base):
    __tablename__ = "schedules"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[int] = mapped_column(Integer, default=2)
    valid_from: Mapped[DateTime] = mapped_column(DateTime, default=date.today())
    valid_for_days: Mapped[int] = mapped_column(Integer, default=30)
    mask_weekdays: Mapped[int] = mapped_column(Integer, default=127)
    mask_weeks: Mapped[int] = mapped_column(BIGINT, default=4503599627370495)
    mask_quartals: Mapped[int] = mapped_column(Integer, default=15)
    mask_days_month: Mapped[int] = mapped_column(Integer, nullable=True)
    nth_weekday: Mapped[int] = mapped_column(Integer, nullable=True)
    nth_index: Mapped[int] = mapped_column(Integer, nullable=True)
    slot_type: Mapped[int] = mapped_column(Integer, default=1)
    slot_min_time: Mapped[int] = mapped_column(Integer, nullable=True)
    slot_max_time: Mapped[int] = mapped_column(Integer, nullable=True)
    slot_step_time: Mapped[int] = mapped_column(Integer, nullable=True)
    hour_start: Mapped[int] = mapped_column(Integer, nullable=True)
    hour_end: Mapped[int] = mapped_column(Integer, nullable=True)
    policy_merge: Mapped[int] = mapped_column(Integer, default=1)
    policy_suggest: Mapped[int] = mapped_column(Integer, default=1)
    rental_id: Mapped[int] = mapped_column(ForeignKey("rentals.id"))
    rental: Mapped["Rental"] = relationship(back_populates="schedules")
    slots: Mapped[List["Slot"]] = relationship()

    def __str__(self):
        return (
            f"SQLA Schedule,"
            f" id: {self.id},"
            f" name: {self.name},"
            f" description: {self.description},"
            f" status: {self.status},"
            f" "
            f" rental: {self.rental.id},"
            f" slots count: {len(self.slots)},"
        )


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
    user: Mapped["User"] = relationship(back_populates="records")
    slot: Mapped["Slot"] = relationship(back_populates="record")

    __table_args__ = (UniqueConstraint("user_id", "slot_id"),)

    def __str__(self):
        return f"SQLA Record, id: {self.id}, user: {self.user.id}, slot: {self.slot.id}"


uri = "postgresql+asyncpg://postgres:qwerty123@127.0.0.1:5432/dev"
engine = create_async_engine(uri, echo=False)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def add_test_data():
    async with AsyncSession(engine) as session:
        user = User(tg_id=103273, username="@telegram_test_user")
        user_2 = User(tg_id=103272, username="@telegram_test_user_2")
        rental = Rental(
            name="Ping-pong table",
            description="Free-to-play ping-pong table on 2nd floor",
            category="SPORT",
        )
        schedule = Schedule(name="Basic",
                            description="Basic schedule for pin-pong table",
                            )
        schedule.rental = rental
        slot = Slot(started_at=datetime(2023, 12, 1, 12, 12), duration=30, status="PLANNED")
        schedule.slots.append(slot)
        record = Record()
        record.slot = slot
        record.user = user
        record_2 = Record(slot_id=1)
        record_2.user = user_2
        session.add_all((user, rental, user_2, schedule, record, record_2))

        await session.commit()


async def main():
    await create_tables()
    await add_test_data()


asyncio.run(main())
