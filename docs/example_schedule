# Пример расписания

- с понедельника по пятницу
- с 9 до 18
- с перерывом с 13 до 14

## Модель 

```python
schedules = {
  "work_days": { # расписание для рабочих дней с 9 до 18 - генерирует хард слоты
    "status": "active",
    "start_date": "2022-02-11",
    "end_date": "2022-02-22",
    "days": [ # с понедельника по пятницу
      1,
      2,
      3,
      4,
      5
    ],
    "weeks": null,
    "months": null,
    "quartals": null,
    "index_days_month": null,
    "day_in_month": null,
    "day_in_year": null,
    "merge_policy": "hard",
    "recommendation_policy": null,
    "start_hour": 9,
    "end_hour": 18,
    "slot_type": "hard", # разрешающий тип слота - хард
    "min_time": 30,
    "max_time": 60
  },
  "rest_time": { # расписание для рабочих дней с 13 до 14 - генерирует занятые слоты - обед!
    "days": [ # с понедельника по пятницу
      1,
      2,
      3,
      4,
      5
    ],
    "weeks": null,
    "months": null,
    "quartals": null,
    "index_days_month": null,
    "day_in_month": null,
    "day_in_year": null,
    "merge_policy": null,
    "recommendation_policy": null,
    "start_hour": 13,
    "end_hour": 14,
    "slot_type": "forbidden", # запрещающий тип слота
    "min_time": null,
    "max_time": null
}
}
```