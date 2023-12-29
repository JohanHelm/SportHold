from enum import IntFlag, IntEnum


DaysOfWeekLangDict = {
    "ru": {
        "Monday": "Пн",
        "Tuesday": "Вт",
        "Wednesday": "Ср",
        "Thursday": "Чт",
        "Friday": "Пт",
        "Saturday": "Сб",
        "Sunday": "Вс",
        "ALL": "Пн-Вс",
    }
}


class DaysOfWeek(IntFlag):
    Monday = 1
    Tuesday = 2
    Wednesday = 4
    Thursday = 8
    Friday = 16
    Saturday = 32
    Sunday = 64
    ALL = 127
    NONE = 0

    def custom_print(self):
        return ",".join(
            DaysOfWeekLangDict["ru"][val.name] for val in DaysOfWeek if self.value & val
        )


class UserRole(IntFlag):
    REGULAR = 1
    PARTNER = 2
    ADMIN = 4
    MANAGER = 8
    EMPLOYEE = 16
    OWNER = 32
    WORKER = 64
    PAID = 128

    def custom_print(self):
        return "|".join(val.name for val in UserRole if self.value & val)


class UserStatus(IntEnum):
    INACTIVE = 0
    ACTIVE = 1

    def custom_print(self):
        return self.name


class SlotStatus(IntEnum):
    INACTIVE = 0
    ACTIVE = 1

    def custom_print(self):
        return self.name


class SlotType(IntEnum):
    ACCESSIBLE = 0
    RESTRICTED = 1

    def custom_print(self):
        return self.name


class ScheduleStatus(IntEnum):
    INACTIVE = 0
    ACTIVE = 1

    def custom_print(self):
        return self.name


class RentalTypes(IntEnum):
    REGULAR = 0

    def custom_print(self):
        return self.name
