from datetime import date
from typing import List
from app.domain.helpers.enums import DaysOfWeek, SlotType
from app.infra.db.models.rental.schema import Rental
from app.infra.db.models.record.schema import Record
from app.infra.db.models.schedule.schema import Schedule
from app.domain.controllers.slots import SlotData


def hello_regular_user(
    user_name: str, avalable_rentals: int, total_rentals: int, records_amount: int
) -> str:
    return (
        f"Вам доступно объектов - {avalable_rentals} из {total_rentals}.\n"
        f"Найдено ваших записей - {records_amount}.\n"
        f"Активная запись\n"
        f"Ближайшая запись\n"
    )


def no_rentals_in_db(avalable_rentals: int, total_rentals: int) -> str:
    return f"Вам доступно объектов - {avalable_rentals} из {total_rentals}.\n"


def hello_owner_user(user_name: str) -> str:
    return (
        f"Привет, {user_name}!\n"
        f"Здесь ты можешь создавать объекты и их распсания, просматривать записи клиентов, пополнять счёт и т.д."
    )


def display_rental_info(rental: Rental, schedules: List[Schedule]) -> str:
    template_rental = f"{rental.name}\n" f"{rental.description}\n\n"

    access_schedule = "Время работы:\n\n"
    restrict_schedule = "Без перерывов!\n\n"
    for schedule in schedules:
        match schedule.slot_type:
            case SlotType.ACCESSIBLE:
                access_schedule += f"📅 c {schedule.started.strftime('%d.%m.%Y')} по {schedule.ended.strftime('%d.%m.%Y')}\n"
                access_schedule += f"📌 {DaysOfWeek(schedule.mask_days).custom_print()}\n" \
                                   f" ⏰ {schedule.hour_start.strftime('%H:%M')} - {schedule.hour_end.strftime('%H:%M')}\n"
            case SlotType.RESTRICTED:
                restrict_schedule = "Перерывы:\n\n"
                restrict_schedule += f"📅 c {schedule.started.strftime('%d.%m.%Y')} по {schedule.ended.strftime('%d.%m.%Y')}\n"
                restrict_schedule += f"📌 {DaysOfWeek(schedule.mask_days).custom_print()}\n" \
                                     f" ⏰ {schedule.hour_start.strftime('%H:%M')} - {schedule.hour_end.strftime('%H:%M')}\n"
    return template_rental + access_schedule + "\n" + restrict_schedule


def display_rental_slots(slot: SlotData) -> str:
    slot_date = slot.started.strftime("%d.%m.%Y г.")
    slot_start_time = slot.started.strftime("%H:%M")
    slot_end_time = slot.ended.strftime("%H:%M")
    return f" Дата: {slot_date}\n" f" Время: {slot_start_time} - {slot_end_time}"


# TODO здесь выводить описание политики бронирования
def display_booking_info(schedule: Schedule, current_date: date) -> str:
    current_date = current_date.strftime("%d.%m.%Y г.")
    return f"Описание брониования: {schedule.description}\n" \
           f"На {current_date}"


def display_user_records(user_records_to_rental: list[Record]) -> str:
    if user_records_to_rental:
        rental = user_records_to_rental[0].rental
        return f"{rental.name}\n" f"{rental.description}\n\n" \
               f"Вы записаны в следующие слоты:\n" \
               f"Нажмите на кнопку чтобы удалить запись."
    else:
        return f"У вас нет актуальных записей."


help_message = (
    f"Краткая инструкция по использованию ботом.\n"
    f"Ссылка на канал с видеоинструкциями.\n"
    f"Ссылка на техподдержку."
)
