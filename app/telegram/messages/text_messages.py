import datetime

from app.infra.db.models.rental.schema import Rental


def hello_regular_user(user_name: str) -> str:
    return f"Привет, {user_name}!\n" \
           f"Далее ты можешь ознакомиться со списком доступных объектов и записаться на свободное время."


def display_rental_info(rental: Rental) -> str:
    return f"Наименование: {rental.name}\n" \
           f"Категория: {rental.category}\n" \
           f"Описание: {rental.description}"


def display_rental_slots(slot: tuple[datetime.datetime, datetime.datetime]) -> str:
    slot_date = slot[0].strftime("%d.%m.%Y г.")
    slot_start_time = slot[0].strftime("%H:%M")
    slot_end_time = slot[1].strftime("%H:%M")
    return f" Дата: {slot_date}\n" \
           f" Время: {slot_start_time} - {slot_end_time}"


help_message = f"Краткая инструкция по использованию ботом.\n" \
               f"Ссылка на канал с видеоинструкциями.\n" \
               f"Ссылка на техподдержку."
