import cx_Oracle
import datetime

# use backslash escapes?
use_bsesc = False

def convertdt(moddt, field_desc):
    """convert Oracle DateTime to Python datetime"""
    year = moddt.year
    month = moddt.month
    day = moddt.day
    hour = moddt.hour
    minute = moddt.minute
    sec = moddt.second
    msec = moddt.fsecond
    pydt = datetime.datetime(year, month, day, hour, minute, sec, msec)
    return pydt
