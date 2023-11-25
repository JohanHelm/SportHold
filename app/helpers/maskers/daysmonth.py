from enum import IntFlag

class DaysInMonth(IntFlag):
    DAY1 = 1
    DAY2 = 2
    DAY3 = 4
    DAY4 = 8
    DAY5 = 16
    DAY6 = 32
    DAY7 = 64
    DAY8 = 128
    DAY9 = 256
    DAY10 = 512
    DAY11 = 1024
    DAY12 = 2048
    DAY13 = 4096
    DAY14 = 8192
    DAY15 = 16384
    DAY16 = 32768
    DAY17 = 65536
    DAY18 = 131072
    DAY19 = 262144
    DAY20 = 524288
    DAY21 = 1048576
    DAY22 = 2097152
    DAY23 = 4194304
    DAY24 = 8388608
    DAY25 = 16777216
    DAY26 = 33554432
    DAY27 = 67108864
    DAY28 = 134217728
    DAY29 = 268435456
    DAY30 = 536870912
    DAY31 = 1073741824
    NONE = 0

def encode_days(days):
    encoded_value = 0
    for day in days:
        encoded_value |= day
    return encoded_value

def decode_days(encoded_value):
    decoded_days = []
    for day in DaysInMonth:
        if day & encoded_value:
            decoded_days.append(day)
    return decoded_days