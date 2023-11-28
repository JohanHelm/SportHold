from enum import IntFlag, auto

class DaysOfWeek(IntFlag): # маска bit'ов, но в int чтобы удобно хранить в бд
    Monday = auto() # 1
    Tuesday = auto() # 2
    Wednesday = auto() # 4
    Thursday = auto() # 8
    Friday = auto() # 16
    Saturday = auto() # 32
    Sunday = auto() # 64
    ALL = 127
    NONE = 0