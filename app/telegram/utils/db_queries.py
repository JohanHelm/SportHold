from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.domain.models.slot.dto import SlotModel, SlotData
from app.infra.db.models.schedule.schema import Schedule
from app.infra.db.models.slot.schema import Slot
from app.infra.db.models.record.schema import Record
from app.infra.db.models.rental.schema import Rental
from app.domain.helpers.enums import ScheduleStatus


async def get_rentals_for_user_count(db_session) -> int:
    async with db_session() as session:
        rental_count = await session.scalar(select(func.count(Rental.id)))
        return rental_count


async def get_records_for_user_count(db_session, user_id) -> int:
    async with db_session() as session:
        records_count = await session.scalar(select(func.count(Record.id)).where(Record.user_id == user_id))
        return records_count


async def get_rental_with_suitable_schedules(db_session, db_offset):
    async with db_session() as session:
        row_rental = await session.execute(
            select(Rental).group_by(Rental.id).offset(db_offset).limit(1)
        )
        current_rental = row_rental.scalar()

        rows_schedules = await session.execute(
            select(Schedule)
            .where(Schedule.rental_id == current_rental.id)
            .where(Schedule.status == ScheduleStatus.ACTIVE)
            .order_by(Schedule.slot_type)
        )

        current_rental_schedules = rows_schedules.scalars().all()
        return current_rental, current_rental_schedules


async def create_slot_in_db(db_session, current_rental: Rental, choosen_slot: SlotModel) -> Slot:
    async with db_session() as session:
        slot = Slot(
            rental_id=current_rental.id,
            schedule_id=choosen_slot.schedule_id,
            started=choosen_slot.started,
            ended=choosen_slot.ended,
            # created=datetime.now(),
        )
        session.add(slot)
        await session.commit()
        await session.refresh(slot)
    return slot


async def create_record_in_db(db_session, user_id, slot: Slot, current_rental: Rental) -> Record:
    async with db_session() as session:
        record = Record(
            user_id=user_id,
            slot_id=slot.id,
            rental_id=current_rental.id,
        )
        session.add(record)
        await session.commit()
        await session.refresh(record)
    return record


async def get_user_records(db_session, user_id) -> list[Record]:
    async with db_session() as session:
        row_records = await session.execute(
            select(Record)
            .where(Record.user_id == user_id)
            .options(selectinload(Record.slot))
            .options(selectinload(Record.rental))
        )
        user_records = row_records.scalars().all()
    return user_records

async def delete_user_record(db_session, record_id) -> None:
    async with db_session() as session:
        await session.execute(Record.__table__.delete().where(Record.id == record_id))
        await session.commit()

