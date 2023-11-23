# Пример расписания

- с понедельника по пятницу
- с 9 до 18
- с перерывом с 13 до 14

## Модель 

```python
schedules = {
  "schedule": { # расписание для рабочих дней с 9 до 18 - генерирует хард слоты
    "name": "name it!"
    "description": "any description here"
    "status": "active",
    "start_date": "2022-02-11",
    "end_date": "2022-02-22",
    "days_mask": 31, # с понедельника по пятницу, 
    "weeks_mask": null,
    "months_mask": null,
    "quartal_masks": null,
    "index_days_month_mask": null,
    "nth_weekday_month_weekday": null,
    "nth_weekday_month_nth": null,
    "day_in_year": null,
    "merge_policy": "hard",
    "suggest_policy": null,
    "start_hour": 9,
    "end_hour": 18,
    "slot_type": "hard", # разрешающий тип слота - хард
    "min_time": 30,
    "max_time": 60
  },
  "schedule": { # расписание для рабочих дней с 13 до 14 - генерирует обед)
    "name": "name it!"
    "description": "any description here"
    "status": "active",
    "start_date": "2022-02-11",
    "end_date": "2022-02-22",
    "days_mask": 31, # с понедельника по пятницу 
    "weeks_mask": null,
    "months_mask": null,
    "quartal_masks": null,
    "index_days_month_mask": null,
    "nth_weekday_month_weekday": null,
    "nth_weekday_month_nth": null,
    "day_in_year": null,
    "merge_policy": "hard",
    "suggest_policy": null,
    "start_hour": 13,
    "end_hour": 14,
    "slot_type": "restrict", # запрещающий тип слота - рестрикт
    "min_time": 30,
    "max_time": 60
  }
}
```