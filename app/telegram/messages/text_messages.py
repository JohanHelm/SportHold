from app.infra.db.models.rental.schema import Rental
from app.infra.db.models.schedule.schema import Schedule
from app.domain.controllers.schedules import TemporarySlot

def hello_regular_user(user_name: str, avalable_rentals: int, total_rentals: int, records_amount: int) -> str:
    return f"Вам доступно объектов - {avalable_rentals} из {total_rentals}.\n" \
           f"Найдено ваших записей - {records_amount}.\n" \
           f"Активная запись\n" \
           f"Ближайшая запись\n"


def hello_owner_user(user_name: str) -> str:
    return f"Привет, {user_name}!\n" \
           f"Здесь ты можешь создавать объекты и их распсания, просматривать записи клиентов, пополнять счёт и т.д."

# TODO в базе schedule.hour_start и schedule.hour_end должны быть datetime или time
def display_rental_info(rental: Rental, schedule: Schedule) -> str:
    # schedule_start_time = schedule.hour_start.strftime("%H:%M")
    # schedule_end_time = schedule.hour_end.strftime("%H:%M")
    return f"Наименование: {rental.name}\n" \
           f"Категория: {rental.category}\n" \
           f"Описание: {rental.description}\n" \
           f"Расписание:\n" \
           f"       Время работы: {schedule.hour_start} - {schedule.hour_end}\n" \
           f"       Cлоты для записи:  {schedule.slot_max_time} минут\n" \
           f"Близжайший свободный слот ---?\n" \
           f"Мои записи на этом объекте"

# TODO здесь выводить описание политики бронирования
def display_booking_info(schedule: Schedule) -> str:
    return f"Описание брониования: {schedule.description}"




help_message = f"Краткая инструкция по использованию ботом.\n" \
               f"Ссылка на канал с видеоинструкциями.\n" \
               f"Ссылка на техподдержку."
