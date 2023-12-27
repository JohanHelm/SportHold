from app.infra.db.models.rental.schema import Rental
from app.domain.controllers.slots import TemporarySlot

def hello_regular_user(user_name: str) -> str:
    return f"Привет, {user_name}!\n" \
           f"Далее ты можешь ознакомиться со списком доступных объектов и записаться на свободное время."

def hello_owner_user(user_name: str) -> str:
    return f"Привет, {user_name}!\n" \
           f"Здесь ты можешь создавать объекты и их распсания, просматривать записи клиентов, пополнять счёт и т.д."


def display_rental_info(rental: Rental) -> str:
    return f"Наименование: {rental.name}\n" \
           f"Категория: {rental.category}\n" \
           f"Описание: {rental.description}"


def display_rental_slots(slot: TemporarySlot) -> str:
    slot_date = slot.start.strftime("%d.%m.%Y г.")
    slot_start_time = slot.start.strftime("%H:%M")
    slot_end_time = slot.end.strftime("%H:%M")
    return f" Дата: {slot_date}\n" \
           f" Время: {slot_start_time} - {slot_end_time}"

help_message = f"Краткая инструкция по использованию ботом.\n" \
               f"Ссылка на канал с видеоинструкциями.\n" \
               f"Ссылка на техподдержку."
