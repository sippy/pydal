import unittest
import datetime
import time
import mx.DateTime
import psycopg

def datetime_equal(mxdt, pydt):
    assert mxdt.year == pydt.year
    assert mxdt.month == pydt.month
    assert mxdt.day == pydt.day
    assert mxdt.hour == pydt.hour
    assert mxdt.minute == pydt.minute
    assert math.floor(mxdt.second) == pydt.second
    assert round(math.modf(mxdt.second)[0] * 1000000) == pydt.microsecond
    return True

def time_equal(mxt, pyt):
    assert mxt.day == 0
    assert mxt.hour == pyt.hour
    assert mxt.minute == pyt.minute
    assert math.floor(mxt.second) == pyt.second
    assert round(math.modf(mxt.second)[0] * 1000000) == pyt.microsecond
    return True

def delta_equal(mxdtd, pydtd):
    assert mxdtd.day == pydtd.days
    mxdtd_sec = int(math.modf(mxdtd.seconds)[1])
    pydtd_sec = pydtd.seconds + pydtd.days * 1440 * 60
    assert mxdtd_sec == pydtd_sec
    mxdtd_msec = int(round(math.modf(mxdtd.seconds)[0] * 1000000))
    assert mxdtd_msec == pydtd.microseconds
    return True

def date_equal(mxd, pyd):
    assert mxd.year == pyd.year
    assert mxd.month == pyd.month
    assert mxd.day == pyd.day
    return True

class Mx2PyDateTimeTest(unittest.TestCase):

    def testCurrentDateTime(self):
        mxnow = mx.DateTime.now()
        pynow = dbtime.mx2pydatetime(mxnow)
        self.assert_(datetime_equal(mxnow, pynow))

    def testTypeDetector(self):
        mxnow = mx.DateTime.now()
        pynow = dbtime.mx2pydt(mxnow)
        self.assert_(datetime_equal(mxnow, pynow))




if __name__ == '__main__':
    import os
    cwd = os.getcwd()
    cwds = cwd.split('/')
    dal_dir = '/'.join(cwds[:-3])
    import sys
    sys.path.insert(0, dal_dir)
    import dal
    unittest.main()
