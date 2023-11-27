from enum import IntFlag, auto

class Quartals(IntFlag): # маска bit'ов, но в int чтобы удобно хранить в бд
    First = 2 # 1
    Second = 4 # 2
    Thrid = 8 # 4
    Fourth = 16 # 8
    ALL = 16+8+4+2
    NONE = 0
