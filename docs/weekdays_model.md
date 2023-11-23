# Модель работы с днем недели

```python
from enum import IntFlag, auto
import datetime

class DaysOfWeek(IntFlag): # маска bit'ов, но в int чтобы удобно хранить в бд
    Monday = auto() # 1
    Tuesday = auto() # 2
    Wednesday = auto() # 4
    Thursday = auto() # 8
    Friday = auto() # 16
    Saturday = auto() # 32
    Sunday = auto() # 64


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