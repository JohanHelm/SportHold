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


class UserStatus(Enum):
    INACTIVE = 0
    ACTIVE = 1
