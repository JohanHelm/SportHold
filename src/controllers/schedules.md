# Генерирование слотов из расписания

## Входные параметры

- от какой даты
- id расписания
- на какой интервал (2 часа)

# Алгоритм без учета рабочих дней и времени работы

- получить из id полный объект расписания
- вытащить минимальное время слота (15 мин)
- получить текущую дату и время, обнулить минуты, обозначить первый слот
- найти время первого слота, для этого к времени первого слота прибавлять минимальный инетрвал
  - до тех пор, пока начало первого слота не перейдет в будущее
- определить остальные слоты, для этого в цикле к первому слоту добавлять минимальный интервал
  - до тех пор, пока начало слота меньше суммы текущего времени и интервала генерации

```python

from datetime import datetime, timedelta

timestep = timedelta(minutes=15)
generated_interval = timedelta(hours=3)

now = datetime.now()

first_slot = datetime(
    year=now.year,
    month=now.month,
    day=now.month,
    hour=now.hour,
    minute=0
)

while True:
    if first_slot < now:
        first_slot = first_slot + timestep
    else:
        break

slots = []
slots.append(first_slot)
current_slot = first_slot + timestep

while True:
    if current_slot < now + generated_interval:
        slots.append(current_slot)
        current_slot = current_slot + timestep
    else:
        break

for slot in slots:
    print(slot)

```
