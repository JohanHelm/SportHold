from enum import IntFlag, auto

class Quartals(IntFlag): # маска bit'ов, но в int чтобы удобно хранить в бд
    First = auto() # 1
    Second = auto() # 2
    Thrid = auto() # 4
    Fourth = auto() # 8
    ALL = 15
    NONE = 0
