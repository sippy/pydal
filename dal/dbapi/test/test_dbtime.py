import unittest
import math
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

class Mx2PyTimeTest(unittest.TestCase):

    def testCurrentTime(self):
        mxdt = mx.DateTime.now()
        mxt = mx.DateTime.Time(mxdt.hour, mxdt.minute, mxdt.second)
        pyt = dbtime.mx2pytime(mxt)
        self.assert_(time_equal(mxt, pyt))

    def testTypeDetector(self):
        mxdt = mx.DateTime.now()
        mxt = mx.DateTime.Time(mxdt.hour, mxdt.minute, mxdt.second)
        pyt = dbtime.mx2pydt(mxt)
        self.assert_(time_equal(mxt, pyt))

class Mx2PyDtDeltaTest(unittest.TestCase):

    def testCurrentDelta(self):
        mxdt = mx.DateTime.now()
        mxdtd = mx.DateTime.DateTimeDelta(1, mxdt.hour, mxdt.minute,
                                          mxdt.second)
        pydtd = dbtime.mx2pydtdelta(mxdtd)
        self.assert_(delta_equal(mxdtd, pydtd))

    def testTypeDetector(self):
        mxdt = mx.DateTime.now()
        mxdtd = mx.DateTime.DateTimeDelta(0, mxdt.hour, mxdt.minute, 
                                          mxdt.second)
        pydtd = dbtime.mx2pydtdelta(mxdtd)
        self.assert_(delta_equal(mxdtd, pydtd))

class Mx2PyDtTest(unittest.TestCase):

    def testCurrentDate(self):
        # same as datetime b/c mx doesn't have a date type
        mxd = mx.DateTime.now()
        pyd = dbtime.mx2pydatetime(mxd)
        self.assert_(date_equal(mxd, pyd))

    def testTypeDetector(self):
        mxd = mx.DateTime.now()
        pyd = dbtime.mx2pydt(mxd)
        self.assert_(date_equal(mxd, pyd))

class Py2MxDtTest(unittest.TestCase):

    def testCurrentDateTime(self):
        pydt = datetime.datetime.now()
        mxdt = dbtime.py2mxdatetime(pydt)
        self.assert_(datetime_equal(mxdt, pydt))

    def testCurrentDate(self):
        # a Python date will be converted to an mx.DateTime.DateTimeType
        pydt = datetime.datetime.now().date()
        mxdt = dbtime.py2mxdatetime(pydt)
        self.assert_(date_equal(mxdt, pydt))

    def testTypeDetector(self):
        pydt = datetime.datetime.now()
        mxdt = dbtime.py2mxdt(pydt)
        self.assert_(datetime_equal(mxdt, pydt))
        # a Python date will be converted to an mx.DateTime.DateTimeType
        pydt = datetime.datetime.now().date()
        mxdt = dbtime.py2mxdt(pydt)
        self.assert_(date_equal(mxdt, pydt))

class Py2MxTimeTest(unittest.TestCase):
    
    def testCurrentTime(self):
        pyt = datetime.datetime.now().time()
        mxt = dbtime.py2mxtime(pyt)
        self.assert_(time_equal(mxt, pyt))

    def testTypeDetector(self):
        pyt = datetime.datetime.now().time()
        mxt = dbtime.py2mxdt(pyt)
        self.assert_(time_equal(mxt, pyt))

class Py2MxDtDeltaTest(unittest.TestCase):
    
    def testCurrentDelta(self):
        pydt = datetime.datetime.now()
        pydtd = datetime.timedelta(0, pydt.second, pydt.microsecond, 0,
                                   pydt.minute, pydt.hour)
        mxdtd = dbtime.py2mxdtdelta(pydtd)
        self.assert_(delta_equal(mxdtd, pydtd))

    def testTypeDetector(self):
        pydt = datetime.datetime.now()
        pydtd = datetime.timedelta(0, pydt.second, pydt.microsecond, 0,
                                   pydt.minute, pydt.hour)
        mxdtd = dbtime.py2mxdt(pydtd)
        self.assert_(delta_equal(mxdtd, pydtd))

# Date and time construction tests

class ConstructDateTest(unittest.TestCase):

    def testCurrentDate(self):
        dt = datetime.datetime.now().date()
        # check Python
        cdt = dbtime.construct_date('py', dt.year, dt.month, dt.day)
        self.assert_(isinstance(cdt, datetime.date))
        self.assert_(not isinstance(cdt, datetime.datetime))
        # check mx
        cdt = dbtime.construct_date('mx', dt.year, dt.month, dt.day)
        self.assert_(isinstance(cdt, mx.DateTime.DateTimeType))

class ConstructTimeTest(unittest.TestCase):
    
    def testCurrentTime(self):
        t = datetime.datetime.now().time()
        ct = dbtime.construct_time('py', t.hour, t.minute, t.second)
        self.assert_(isinstance(ct, datetime.time))
        ct = dbtime.construct_time('mx', t.hour, t.minute, t.second)
        self.assert_(isinstance(ct, mx.DateTime.DateTimeDeltaType))

class ConstructTimeStampTest(unittest.TestCase):
    
    def testCurrentDateTime(self):
        dt = datetime.datetime.now()
        cdt = dbtime.construct_timestamp('py', dt.year, dt.month, dt.day,
                                         dt.hour, dt.minute, dt.second)
        self.assert_(isinstance(cdt, datetime.datetime))
        cdt = dbtime.construct_timestamp('mx', dt.year, dt.month, dt.day,
                                         dt.hour, dt.minute, dt.second)
        self.assert_(isinstance(cdt, mx.DateTime.DateTimeType))

class ConstructDateFromTicksTest(unittest.TestCase):
    
    def testCurrentDate(self):
        ticks = time.time()
        date = datetime.date.fromtimestamp(ticks)
        cdate = dbtime.construct_datefromticks('py', ticks)
        self.assert_(isinstance(cdate, datetime.date))
        self.assert_(not isinstance(cdate, datetime.datetime))
        self.assertEqual(date, cdate)
        date = mx.DateTime.DateFromTicks(ticks)
        cdate = dbtime.construct_datefromticks('mx', ticks)
        self.assert_(isinstance(cdate, mx.DateTime.DateTimeType))
        self.assertEqual(date, cdate)

class ConstructTimeFromTicksTest(unittest.TestCase):
    
    def testCurrentTime(self):
        ticks = time.time()
        nowtime = datetime.datetime.fromtimestamp(ticks).time()
        cnowtime = dbtime.construct_timefromticks('py', ticks)
        self.assert_(isinstance(cnowtime, datetime.time))
        self.assertEqual(nowtime, cnowtime)
        nowtime = mx.DateTime.TimeFromTicks(ticks)
        cnowtime = dbtime.construct_timefromticks('mx', ticks)
        self.assert_(isinstance(cnowtime, mx.DateTime.DateTimeDeltaType))
        self.assertEqual(nowtime, cnowtime)

class ConstructTimeStampFromTicksTest(unittest.TestCase):
    
    def testCurrentDate(self):
        ticks = time.time()
        dt = datetime.datetime.fromtimestamp(ticks)
        ##dt = dt.replace(microsecond=0)
        cdt = dbtime.construct_timestampfromticks('py', ticks)
        self.assert_(isinstance(cdt, datetime.datetime))
        self.assertEqual(dt, cdt)
        dt = mx.DateTime.localtime(ticks)
        cdt = dbtime.construct_timestampfromticks('mx', ticks)
        self.assert_(isinstance(cdt, mx.DateTime.DateTimeType))
        self.assertEqual(dt, cdt)

# Other functions

class Native2Pref(unittest.TestCase):

    # to datetime.datetime type

    def testMx2PyDateTime(self):
        mxdt = mx.DateTime.now()
        pydt = dbtime.native2pref(mxdt, 'py')
        self.assert_(isinstance(pydt, datetime.datetime))

    def testPy2PyDateTime(self):
        # request the same type
        pydt1 = datetime.datetime.now()
        pydt2 = dbtime.native2pref(pydt1, 'py')
        self.assert_(isinstance(pydt2, datetime.datetime))
        self.assertEqual(pydt1, pydt2)

    def testStr2PyDateTime(self):
        strdt = '12/24/2004 00:00:01'
        pydt1 = datetime.datetime(2004, 12, 24, 0, 0, 1)
        pydt2 = dbtime.native2pref(strdt, 'py')
        self.assertEqual(pydt1, pydt2)

    # to mx.DateTimeType

    def testPy2MxDateTime(self):
        pydt = datetime.datetime.now()
        mxdt = dbtime.native2pref(pydt, 'mx')
        self.assert_(isinstance(mxdt, mx.DateTime.DateTimeType))

    def testMx2MxDateTime(self):
        mxdt1 = mx.DateTime.now() 
        mxdt2 = dbtime.native2pref(mxdt1, 'mx')
        self.assertEqual(mxdt1, mxdt2)

    def testStr2MxDateTime(self):
        strdt = '12/24/2004 00:00:01'
        mxdt1 = mx.DateTime.DateTime(2004, 12, 24, 0, 0, 1)
        mxdt2 = dbtime.native2pref(strdt, 'mx')
        self.assertEqual(mxdt1, mxdt2)

    # to datetime.date type

    def testPy2PyDate(self):
        # request the same type
        pydt1 = datetime.datetime.now().date()
        pydt2 = dbtime.native2pref(pydt1, 'py')
        self.assert_(not isinstance(pydt2, datetime.datetime))
        self.assert_(isinstance(pydt2, datetime.date))
        self.assertEqual(pydt1, pydt2)

    def testStr2PyDate(self):
        strdt = '12/24/2004'
        pydt1 = datetime.date(2004, 12, 24)
        pydt2 = dbtime.native2pref(strdt, 'py')
        self.assertEqual(pydt1, pydt2)

    # to datetime.time type

    def testMx2PyTime(self):
        mxdt = mx.DateTime.now()
        mxt = mx.DateTime.Time(mxdt.hour, mxdt.minute, mxdt.second)
        pyt1 = dbtime.mx2pytime(mxt)
        pyt2 = dbtime.native2pref(mxt, 'py')
        self.assert_(isinstance(pyt2, datetime.time))
        self.assertEqual(pyt1, pyt2)

    def testPy2PyTime(self):
        # request the same type
        pydt1 = datetime.datetime.now().time()
        pydt2 = dbtime.native2pref(pydt1, 'py')
        self.assert_(isinstance(pydt2, datetime.time))
        self.assertEqual(pydt1, pydt2)

    def testStr2PyDate(self):
        strdt = '12:21:32 AM'
        pydt1 = datetime.time(12, 21, 32)
        pydt2 = dbtime.native2pref(strdt, 'py')
        self.assertEqual(pydt1, pydt2)

    # to mx.time type (actuall datetimedelta)

    def testPy2MxTime(self):
        pyt = datetime.datetime.now().time()
        mxt1 = dbtime.py2mxtime(pyt)
        mxt2 = dbtime.native2pref(mxt1, 'mx')
        self.assert_(isinstance(mxt2, mx.DateTime.DateTimeDeltaType))
        self.assertEqual(mxt1, mxt2)

    def testMx2MxTime(self):
        # request the same type
        mxdt = mx.DateTime.now()
        mxt1 = mx.DateTime.Time(mxdt.hour, mxdt.minute, mxdt.second)
        mxt2 = dbtime.native2pref(mxt1, 'mx')
        self.assert_(isinstance(mxt2, mx.DateTime.DateTimeDeltaType))
        self.assertEqual(mxt1, mxt2)

    def testStr2MxDate(self):
        strdt = '12:21:32 AM'
        mxt1 = mx.DateTime.Time(12, 21, 32)
        mxt2 = dbtime.native2pref(strdt, 'mx')
        self.assertEqual(mxt1, mxt2)

    def testCustomType(self):
        pass

class DtClass(unittest.TestCase):

    def testPy(self):
        # Python
        pydt = datetime.datetime.now()
        pyd = pydt.date()
        pyt = pydt.time()
        self.failUnless(dbtime.dtclass(pydt) == 'py')
        self.failUnless(dbtime.dtclass(pyd) == 'py')
        self.failUnless(dbtime.dtclass(pyt) == 'py')

    def testMx(self):
        # Python
        mxdt = mx.DateTime.now()
        mxd = mx.DateTime.Date(2004, 01, 01)
        mxt = mx.DateTime.Time(12, 30, 01)
        self.failUnless(dbtime.dtclass(mxdt) == 'mx')
        self.failUnless(dbtime.dtclass(mxd) == 'mx')
        self.failUnless(dbtime.dtclass(mxt) == 'mx')

    def testOtherInput(self):
        strdt = '12/12/2004'
        result = dbtime.dtclass(strdt)
        self.failUnless(result == None)

class DtSubNative(unittest.TestCase):

    def testPyPyscopg(self):
        dt = datetime.datetime.now()
        params = [1, 2, 3, dt]
        result = dbtime.dtsubnative('py', psycopg, params)
        # how do I check this ?


if __name__ == '__main__':
    import os
    cwd = os.getcwd()
    cwds = cwd.split('/')
    dal_dir = '/'.join(cwds[:-3])
    import sys
    sys.path.insert(0, dal_dir)
    from dal.dbapi import dbtime
    unittest.main()
