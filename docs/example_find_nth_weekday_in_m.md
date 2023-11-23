```python

from datetime import datetime, timedelta

def find_nth_weekday_in_month(year, month, weekday, n):
    # Находим первый день недели в месяце
    d = datetime(year, month, 1)
    while d.weekday() != weekday:
        d += timedelta(days=1)

    # Переходим к нужной неделе
    d += timedelta(weeks=n-1)

    # Возвращаем дату
    return d

year = 2023  # Пример: текущий год
month = 11  # Пример: февраль
weekday = 0  # Понедельник
n = 2  # Второй

result = find_nth_weekday_in_month(year, month, weekday, n)
print(result.strftime('%Y-%m-%d'))

```