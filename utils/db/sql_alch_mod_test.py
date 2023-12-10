import asyncio
from datetime import date, datetime, timedelta
from typing import List
from enum import IntFlag, IntEnum
from sqlalchemy import (
    DateTime,
    UniqueConstraint,
    Integer,
    String,
    ForeignKey,
    BIGINT,
    ARRAY
)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass

class UserRole(IntFlag):
    REGULAR = 1
    PARTNER = 2
    ADMIN = 4
    MANAGER = 8
    EMPLOYEE = 16
    OWNER = 32
    WORKER = 64
    PAID = 128

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String)
    fullname: Mapped[str] = mapped_column(String)
    lang_code: Mapped[str] = mapped_column(String)
    registration_date: Mapped[DateTime] = mapped_column(DateTime)
    active: Mapped[int] = mapped_column(Integer, default=1)
    roles: Mapped["UserRole"] = mapped_column(Integer, default=1)
    records: Mapped[List["Record"]] = relationship()

    def __str__(self):
        return f"SQLA User, " \
               f"id: {self.user_id}, " \
               f"username: {self.username}, " \
               f"active records count: {len(self.records)}"


class Rental(Base):
    __tablename__ = "rentals"

    rental_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    schedules: Mapped[List["Schedule"]] = relationship()

    def __str__(self):
        return f"SQLA Rental, " \
               f"id: {self.id}, " \
               f"category: {self.category}, " \
               f"name: {self.name}, " \
               f"description: {self.description}, " \
               f"schedules count: {len(self.schedules)}"


class Schedule(Base):
    __tablename__ = "schedules"

    schedule_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
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
    rental_id: Mapped[int] = mapped_column(ForeignKey("rentals.rental_id"))
    rental: Mapped["Rental"] = relationship(back_populates="schedules")
    slots: Mapped[List["Slot"]] = relationship()

    def __str__(self):
        return (
            f"SQLA Schedule,"
            f" id: {self.rental_id},"
            f" name: {self.name},"
            f" description: {self.description},"
            f" status: {self.status},"
            f" "
            f" rental: {self.rental.id},"
            f" slots count: {len(self.slots)},"
        )


class Slot(Base):
    __tablename__ = "slots"

    slot_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    started_at: Mapped[DateTime] = mapped_column(DateTime)
    duration: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(
        String
    )  # TODO: вынести статусы в отдельный перечень
    schedule_id: Mapped[int] = mapped_column(ForeignKey("schedules.schedule_id"))
    record: Mapped[List["Record"]] = relationship()
    schedule: Mapped["Schedule"] = relationship(back_populates="slots")

    def __str__(self):
        return f"SQLA Slot, " \
               f"id: {self.id}, " \
               f"schedule: {self.schedule.id}, " \
               f"records: {[str(x) for x in self.record]}, " \
               f"start at: {self.started_at}, " \
               f"duration: {self.duration}, " \
               f"status: {self.status}"


class Record(Base):
    __tablename__ = "records"

    record_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), unique=False)
    slot_id: Mapped[int] = mapped_column(ForeignKey("slots.slot_id"), unique=False)
    user: Mapped["User"] = relationship(back_populates="records")
    slot: Mapped["Slot"] = relationship(back_populates="record")

    __table_args__ = (UniqueConstraint("user_id", "slot_id"),)

    def __str__(self):
        return f"SQLA Record, id: {self.record_id}, user: {self.user.user_id}, slot: {self.slot.slot_id}"


class Tarif(Base):
    __tablename__ = "tarifs"

    rentals_amount: Mapped[int] = mapped_column(primary_key=True)
    one_month: Mapped[int] = mapped_column(Integer)
    three_month: Mapped[int] = mapped_column(Integer)
    six_month: Mapped[int] = mapped_column(Integer)
    one_year: Mapped[int] = mapped_column(Integer)
    two_years: Mapped[int] = mapped_column(Integer)
    three_years: Mapped[int] = mapped_column(Integer)

    def __str__(self):
        return (
            f"SQLA Tarif,"
            f" tarif: {self.rentals_amount},"
            f" one_month: {self.one_month},"
            f" six_month: {self.six_month},"
            f" one_year: {self.one_year},"
            f" two_years: {self.two_years},"
            f" three_years: {self.three_years}"
        )


class Promo(Base):
    __tablename__ = "promos"

    promo_code: Mapped[str] = mapped_column(primary_key=True)
    active: Mapped[int] = mapped_column(Integer, default=1)
    promo_money: Mapped[int] = mapped_column(Integer)
    used_times: Mapped[int] = mapped_column(Integer, default=0)
    expires_at: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    times_to_use: Mapped[int] = mapped_column(Integer, nullable=True)

    def __str__(self):
        return (
            f"SQLA Promo,"
            f" promo_code: {self.promo_code},"
            f" active: {self.active},"
            f" promo_money: {self.promo_money},"
            f" used_times: {self.used_times},"
            f" expires_at: {self.expires_at},"
            f" times_to_use: {self.times_to_use}"
        )


class Income(Base):
    __tablename__ = "incomes"

    income_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(Integer)  # TODO реализовать завсимость от столбца с первичным ключом в таблице users
    full_name: Mapped[str] = mapped_column(String)
    summ: Mapped[int] = mapped_column(Integer)
    date_time: Mapped[DateTime] = mapped_column(DateTime)
    method: Mapped[int] = mapped_column(Integer)

    def __str__(self):
        return (
            f"SQLA Income,"
            f" customer_id: {self.customer_id},"
            f" full_name: {self.full_name},"
            f" summ: {self.summ},"
            f" date_time: {self.date_time},"
        )

class Order(Base):
    __tablename__ = "orders"

    order_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(Integer)   # TODO реализовать завсимость от столбца с первичным ключом в таблице users
    full_name: Mapped[str] = mapped_column(String)
    tarif: Mapped[int] = mapped_column(Integer)  # TODO реализовать зависимость от таблицы с тарифами
    date_time: Mapped[DateTime] = mapped_column(DateTime)
    duration: Mapped[int] = mapped_column(Integer)
    active: Mapped[int] = mapped_column(Integer, default=1)
    prolong: Mapped[int] = mapped_column(Integer, default=1)

    def __str__(self):
        return (
            f"SQLA Order,"
            f" order_id: {self.order_id},"
            f" customer_id: {self.customer_id},"
            f" full_name: {self.full_name},"
            f" tarif: {self.tarif},"
            f" date_time: {self.date_time},"
            f" expires_at: {self.expires_at},"
            f" duration: {self.duration},"
            f" active: {self.active},"
            f" prolong: {self.prolong}"
        )

uri = "postgresql+asyncpg://postgres:qwerty123@127.0.0.1:5432/dev"
engine = create_async_engine(uri, echo=False)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def add_test_data():
    async with AsyncSession(engine) as session:
        user = User(user_id=103273, username="@telegram_test_user", fullname="Rocky Balboa", lang_code="ru",
                    registration_date=datetime.now(), active=0)
        user_2 = User(user_id=103272, username="@telegram_test_user_2", fullname="Ivan Drago", lang_code="ru",
                    registration_date=datetime.now())
        rental = Rental(
            name="Ping-pong table",
            description="Free-to-play ping-pong table on 2nd floor",
            category="SPORT",
        )
        rental1 = Rental(
            name="Exercise bike",
            description="New power generating facility, birn you fat and save couple of weals.",
            category="SPORT",
        )
        rental2 = Rental(
            name="Darts board",
            description="Spend some time by throwing arrows",
            category="SPORT",
        )

        schedule = Schedule(name="Basic",
                            description="Basic schedule for pin-pong table",
                            )
        schedule.rental = rental
        schedule1 = Schedule(name="Basic",
                            description="Basic schedule for exercise bike",
                            )
        schedule1.rental = rental1
        schedule2 = Schedule(name="Common",
                             description="Common schedule for different rentals",
                             )
        schedule2.rental = rental2
        slot = Slot(started_at=datetime(2023, 12, 1, 12, 12), duration=30, status="PLANNED")
        schedule.slots.append(slot)
        record = Record()
        record.slot = slot
        record.user = user
        record_2 = Record(slot_id=1)
        record_2.user = user_2
        tarif1 = Tarif(rentals_amount=1,
                       one_month=150,
                       three_month=400,
                       six_month=750,
                       one_year=1500,
                       two_years=2500,
                       three_years=3500)
        promo_test = Promo(promo_code='TEST_PROMO', promo_money=100, times_to_use=5)
        income1 = Income(customer_id=103272, full_name="John Doe", summ=100, date_time=datetime.now(), method=1)
        order1 = Order(customer_id=103272, full_name="John Doe", tarif=1, date_time=datetime.now(), duration=1, active=1, prolong=1)
        setattr(user, 'active', 1)
        session.add_all((user, rental, user_2, schedule, record, record_2, tarif1, promo_test, income1, order1, rental1, rental2))

        await session.commit()


async def main():
    await create_tables()
    await add_test_data()


asyncio.run(main())
