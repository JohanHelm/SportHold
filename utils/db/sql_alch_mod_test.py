import asyncio
from datetime import time

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from app.infra.db.models import *
from app.domain.helpers.enums import ScheduleStatus, SlotType, DaysOfWeek

uri = "postgresql+asyncpg://postgres:qwerty123@127.0.0.1:5432/dev"
engine = create_async_engine(uri, echo=False)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def add_test_data():
    async with AsyncSession(engine) as session:
        user = User(id=103273, username="@telegram_test_user", fullname="Rocky Balboa")
        user_2 = User(id=103272, username="@telegram_test_user_2", fullname="Ivan Drago")
        rental = Rental(
            name="Ping-pong table",
            description="Free-to-play ping-pong table on 2nd floor",
        )
        rental1 = Rental(
            name="Exercise bike",
            description="New power generating facility, birn you fat and save couple of weals.",
        )
        rental2 = Rental(
            name="Darts board",
            description="Spend some time by throwing arrows",
        )

        schedule = Schedule(name="Basic",
                            description="Basic schedule for pin-pong table",
                            status=ScheduleStatus.ACTIVE,
                            )
        schedule.rental = rental
        schedule0 = Schedule(name="Basic_break",
                             description="Basic schedule for pin-pong table break",
                             slot_type=SlotType.RESTRICTED,
                             hour_start=time(13),
                             hour_end=time(14),
                             status=ScheduleStatus.ACTIVE,
                             )
        schedule0.rental = rental
        schedule1 = Schedule(name="Basic",
                             description="Basic schedule for exercise bike",
                             status=ScheduleStatus.ACTIVE,
                            )
        schedule1.rental = rental1
        schedule2 = Schedule(name="Common",
                             description="Common schedule for different rentals",
                             status=ScheduleStatus.ACTIVE,
                             )
        schedule2.rental = rental2
        # slot = Slot(started_at=datetime(2023, 12, 1, 12, 12), duration=30, status="PLANNED")
        # schedule.slots.append(slot)
        # record = Record()
        # record.slot = slot
        # record.user = user
        # record_2 = Record(slot_id=1)
        # record_2.user = user_2
        # tarif1 = Tarif(rentals_amount=1,
        #                one_month=150,
        #                three_month=400,
        #                six_month=750,
        #                one_year=1500,
        #                two_years=2500,
        #                three_years=3500)
        # promo_test = Promo(promo_code='TEST_PROMO', promo_money=100, times_to_use=5)
        # income1 = Income(customer_id=103272, full_name="John Doe", summ=100, date_time=datetime.now(), method=1)
        # order1 = Order(customer_id=103272, full_name="John Doe", tarif=1, date_time=datetime.now(), duration=1, active=1, prolong=1)
        #
        # session.add(user)
        session.add_all((user, user_2, rental, rental1, rental2, schedule, schedule1, schedule2)) # record, record_2, tarif1, promo_test, income1, order1, ))

        await session.commit()


async def main():
    await create_tables()
    await add_test_data()


asyncio.run(main())

# print(UserStatus.ACTIVE)
# print(UserRole.REGULAR)
# print(type(UserStatus.ACTIVE))
# print(type(UserRole.REGULAR))