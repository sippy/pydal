import unittest
import datetime
import mx.DateTime
import time

class Initialization(unittest.TestCase):

    def setUp(self):
        self.dbmod = dal.wrapdriver('MySQLdb')

    def testModGlobals(self):
        dbmod = self.dbmod
        self.assert_(dbmod.apilevel == '2.0')
        self.assert_(dbmod.threadsafety == 0)
        self.assert_(dbmod.paramstyle == 'qmark')

    def testModSingletons(self):
        dbmod = self.dbmod
        self.assert_(hasattr(dbmod, 'STRING'))
        self.assert_(hasattr(dbmod, 'BINARY'))
        self.assert_(hasattr(dbmod, 'NUMBER'))
        self.assert_(hasattr(dbmod, 'DATETIME'))
        self.assert_(hasattr(dbmod, 'ROWID'))

    def testExceptionPassThru(self):
        driver = self.dbmod._driver
        self.assert_(issubclass(driver.Warning, dal.Warning))
        self.assert_(issubclass(driver.Error, dal.Error))
        self.assert_(issubclass(driver.InterfaceError, dal.InterfaceError))
        self.assert_(issubclass(driver.DatabaseError, dal.DatabaseError))
        self.assert_(issubclass(driver.DataError, dal.DataError))
        self.assert_(issubclass(driver.OperationalError,
                                dal.OperationalError))
        self.assert_(issubclass(driver.IntegrityError, dal.IntegrityError))
        self.assert_(issubclass(driver.InternalError, dal.InternalError))
        self.assert_(issubclass(driver.ProgrammingError,
                                dal.ProgrammingError))
        self.assert_(issubclass(driver.NotSupportedError,
                                dal.NotSupportedError))

    # test the date constructors

    def testCurrentDate(self):
        dbmod = self.dbmod
        dt = datetime.datetime.now().date()
        # check Python
        dbmod.dtmod = 'py'
        cdt = dbmod.Date(dt.year, dt.month, dt.day)
        self.assert_(isinstance(cdt, datetime.date))
        self.assert_(not isinstance(cdt, datetime.datetime))
        # check mx
        dbmod.dtmod = 'mx'
        cdt = dbmod.Date(dt.year, dt.month, dt.day)
        self.assert_(isinstance(cdt, mx.DateTime.DateTimeType))

    def testCurrentTime(self):
        dbmod = self.dbmod
        dbmod.dtmod = 'py'
        t = datetime.datetime.now().time()
        ct = dbmod.Time(t.hour, t.minute, t.second)
        self.assert_(isinstance(ct, datetime.time))
        dbmod.dtmod = 'mx'
        ct = dbmod.Time(t.hour, t.minute, t.second)
        self.assert_(isinstance(ct, mx.DateTime.DateTimeDeltaType))

    def testCurrentDateTime(self):
        dbmod = self.dbmod
        dbmod.dtmod = 'py'
        dt = datetime.datetime.now()
        cdt = dbmod.Timestamp(dt.year, dt.month, dt.day,
                                         dt.hour, dt.minute, dt.second)
        self.assert_(isinstance(cdt, datetime.datetime))
        dbmod.dtmod = 'mx'
        cdt = dbmod.Timestamp(dt.year, dt.month, dt.day,
                                         dt.hour, dt.minute, dt.second)
        self.assert_(isinstance(cdt, mx.DateTime.DateTimeType))

    def testCurrentDateFromTicks(self):
        dbmod = self.dbmod
        dbmod.dtmod = 'py'
        ticks = time.time()
        date = datetime.date.fromtimestamp(ticks)
        cdate = dbmod.DateFromTicks(ticks)
        self.assert_(isinstance(cdate, datetime.date))
        self.assert_(not isinstance(cdate, datetime.datetime))
        self.assertEqual(date, cdate)
        date = mx.DateTime.DateFromTicks(ticks)
        dbmod.dtmod = 'mx'
        cdate = dbmod.DateFromTicks(ticks)
        self.assert_(isinstance(cdate, mx.DateTime.DateTimeType))
        self.assertEqual(date, cdate)

    def testCurrentTimeFromTicks(self):
        dbmod = self.dbmod
        dbmod.dtmod = 'py'
        ticks = time.time()
        nowtime = datetime.datetime.fromtimestamp(ticks).time()
        cnowtime = dbmod.TimeFromTicks(ticks)
        self.assert_(isinstance(cnowtime, datetime.time))
        self.assertEqual(nowtime, cnowtime)
        nowtime = mx.DateTime.TimeFromTicks(ticks)
        dbmod.dtmod = 'mx'
        cnowtime = dbmod.TimeFromTicks(ticks)
        self.assert_(isinstance(cnowtime, mx.DateTime.DateTimeDeltaType))
        self.assertEqual(nowtime, cnowtime)

    def testCurrentTimestampFromTicks(self):
        dbmod = self.dbmod
        dbmod.dtmod = 'py'
        ticks = time.time()
        dt = datetime.datetime.fromtimestamp(ticks)
        ##dt = dt.replace(microsecond=0)
        cdt = dbmod.TimestampFromTicks(ticks)
        self.assert_(isinstance(cdt, datetime.datetime))
        self.assertEqual(dt, cdt)
        dt = mx.DateTime.localtime(ticks)
        dbmod.dtmod = 'mx'
        cdt = dbmod.TimestampFromTicks(ticks)
        self.assert_(isinstance(cdt, mx.DateTime.DateTimeType))
        self.assertEqual(dt, cdt)


    def tearDown(self):
        del self.dbmod

def main():
    dbmod = dal.wrapdriver('MySQLdb')
    cn = dbmod.connect(db='dball', user='randall', passwd='arnold1')
    cs = cn.cursor()
    cs.use_db_row = True
    dbmod.paramstyle = 'numeric'
    query = 'select * from test1 where TS1 > :1'
    #query = 'select * from test1'
    ##query = []
    ##query.append('select * from test1 where TS1 > ')
    ##query.append(dbmod.Date(2004, 01, 01))
    ##query.append('order by name')
    params = [dbmod.Date(2004, 01, 01)]
    cs.execute(query, params)
    #cs.execute(query)
    result = cs.fetchall()
    print(result)


if __name__ == '__main__':
    import os
    cwd = os.getcwd()
    cwds = cwd.split('/')
    dal_dir = '/'.join(cwds[:-3])
    import sys
    sys.path.insert(0, dal_dir)
    import dal
    unittest.main()
