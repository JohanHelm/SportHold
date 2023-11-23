# Модель работы с днем недели

```python
from enum import IntFlag, auto
import datetime

class DaysOfWeek(IntFlag):
    Monday = auto()
    Tuesday = auto()
    Wednesday = auto()
    Thursday = auto()
    Friday = auto()
    Saturday = auto()
    Sunday = auto()


weekdays = {
    1: DaysOfWeek.Monday,
    2: DaysOfWeek.Tuesday,
    3: DaysOfWeek.Wednesday,
    4: DaysOfWeek.Thursday,
    5: DaysOfWeek.Friday,
    6: DaysOfWeek.Saturday,
    7: DaysOfWeek.Sunday,
}

work_days =  DaysOfWeek.Monday| DaysOfWeek.Tuesday| DaysOfWeek.Wednesday| DaysOfWeek.Thursday| DaysOfWeek.Friday



datetime.datetime.today()
datetime.datetime(2012, 3, 23, 23, 24, 55, 173504)
x = weekdays[datetime.datetime.today().isoweekday()]

print(x in work_days)
```