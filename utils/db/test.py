from datetime import datetime, timedelta
from typing import List
from pydantic import BaseModel


class Schedule(BaseModel):
    id: int
    name: str
    description: str
    active: bool
    user_id: int
    conditions: List["Condition"]
    manual_time_slots: List["ManualTimeSlot"]


class Condition(BaseModel):
    id: int
    start_time: datetime
    end_time: datetime
    days_of_week: List[int]
    min_duration: int
    max_duration: int


class ManualTimeSlot(BaseModel):
    id: int
    start_time: datetime
    end_time: datetime


def generate_time_slots(schedules: List[Schedule]) -> List[tuple]:
    time_slots = []

    for schedule in schedules:
        if not schedule.active:
            continue

        for condition in schedule.conditions:
            start_time = condition.start_time
            end_time = condition.end_time
            days_of_week = condition.days_of_week
            min_duration = condition.min_duration
            max_duration = condition.max_duration

            current_time = start_time
            while current_time + timedelta(minutes=max_duration or 0) <= end_time:
                if current_time.weekday() in days_of_week:
                    duration = max_duration
                    if current_time + timedelta(minutes=duration) <= end_time:
                        time_slots.append(
                            (
                                current_time,
                                current_time + timedelta(minutes=duration),
                            )
                        )
                current_time += timedelta(minutes=max_duration)

        manual_slots = schedule.manual_time_slots
        for manual_slot in manual_slots:
            manual_start = manual_slot.start_time
            manual_end = manual_slot.end_time
            overlapping_slots = []
            for slot_start, slot_end in time_slots:
                if manual_start < slot_end and manual_end > slot_start:
                    overlapping_slots.append((slot_start, slot_end))
            for slot_start, slot_end in overlapping_slots:
                time_slots.remove((slot_start, slot_end))
            time_slots.append((manual_start, manual_end))

    # Добавление слотов с min_duration между сгенерированными интервалами
    final_time_slots = []
    for i, (slot_start, slot_end) in enumerate(time_slots):
        final_time_slots.append((slot_start, slot_end))
        if i < len(time_slots) - 1:
            next_slot_start = time_slots[i + 1][0]
            if next_slot_start - slot_end >= timedelta(minutes=min_duration):
                final_time_slots.append(
                    (slot_end, slot_end + timedelta(minutes=min_duration))
                )
            elif next_slot_start - slot_end >= timedelta(minutes=1):
                final_time_slots[-1] = (slot_start, next_slot_start)

    return final_time_slots


# Тестирование функции generate_time_slots

# Создаем объекты расписания, условий и вручную добавленных временных слотов
schedule1 = Schedule(
    id=1,
    name="Schedule 1",
    description="Description 1",
    active=True,
    user_id=1,
    conditions=[
        Condition(
            id=1,
            start_time=datetime(2022, 1, 1, 9, 0),
            end_time=datetime(2022, 1, 1, 17, 0),
            days_of_week=[0, 1, 3, 4, 5, 6, 7, 2],
            min_duration=30,
            max_duration=60,
        )
    ],
    manual_time_slots=[
        ManualTimeSlot(
            id=1,
            start_time=datetime(2022, 1, 1, 13, 5),
            end_time=datetime(2022, 1, 1, 14, 35),
        )
    ],
)

# Передаем список расписаний в функцию для формирования временных слотов
time_slots = generate_time_slots([schedule1])

# Выводим результат
for time_slot in sorted(time_slots):
    start_time, end_time = time_slot
    print(f"Time Slot: {start_time} - {end_time}")
