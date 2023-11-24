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
    "valid_from": "2022-02-11",
    "valid_to": "2022-02-22",
    "mask_weekdays": 31, # с понедельника по пятницу, 
    "mask_weeks": null,
    "mask_quratals": null,
    "quartal_masks": null,
    "mask_days_month": null,
    "nth_weekday": null,
    "nth_index": null,
    "mask_days_year": null,
    "policy_merge": "hard",
    "policy_suggest": null,
    "hour_start": 9,
    "hour_end": 18,
    "slot_type": "hard", # разрешающий тип слота - хард
    "slot_min_time": 30,
    "slot_max_time": 60,
    "slot_step_time": 5
  },
  "schedule": { # расписание для рабочих дней с 13 до 14 - 
    "name": "name it!"
    "description": "any description here"
    "status": "active",
    "valid_from": "2022-02-11",
    "valid_to": "2022-02-22",
    "mask_weekdays": 31, # с понедельника по пятницу, 
    "mask_weeks": null,
    "mask_quratals": null,
    "quartal_masks": null,
    "mask_days_month": null,
    "nth_weekday": null,
    "nth_index": null,
    "mask_days_year": null,
    "policy_merge": "hard",
    "policy_suggest": null,
    "hour_start": 13,
    "hour_end": 14,
    "slot_type": "restrict", # запрещающий тип слота - хард
    "slot_min_time": 30,
    "slot_max_time": 60,
    "slot_step_time": 5
  }
}
```