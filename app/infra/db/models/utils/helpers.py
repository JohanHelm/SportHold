from enum import Enum, IntFlag


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


class UserStatus(Enum):
    INACTIVE = 0
    ACTIVE = 1

    def custom_print(self):
        return self.name


class SlotStatus(Enum):
    INACTIVE = 0
    ACTIVE = 1

    def custom_print(self):
        return self.name


class SlotType(Enum):
    ACCESSIBLE = 0
    RESTRICTED = 1

    def custom_print(self):
        return self.name


class ScheduleStatus(Enum):
    INACTIVE = 0
    ACTIVE = 1

    def custom_print(self):
        return self.name
