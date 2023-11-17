
from calendar import MONDAY
from enum import Enum
from typing import List
from pydantic import BaseModel
from pydantic.types import datetime

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
    day: datetime
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


condition = Conditions(
    type=ConditionType.solid_slot,
    start_at=datetime(2023, 11, 16),
    end_at=datetime(2023, 11, 17),
    work_days=[WorkDays.monday],
    exceptions = [],
    start_hour=9,
    end_hour=21,
    min_time=15,
    max_time=30,
    book_range_hours = 24
)

def generate_slots_from_condition(condition):
    if not (condition.type == ConditionType.solid_slot):
        return 1
    if not (condition.start_at <=datetime.now() < condition.end_at):
        return 2
    
    # смотрим, на какое время вперед надо генерировать слоты
    # генерируем слоты по min_time
    # получаем текущие слоты и удаляем их из сгенерированных слотов
    # вуаля, вы прекрасны


def main():
    s = generate_slots_from_condition(condition)
    print(s)
if __name__ == "__main__":
    main()