import MySQLdb
import datetime
import math

# use backslash escapes?
use_bsesc = True

def init1(wrapper):
    # MySQLDb does not define DATETIME
    wrapper._driver.DATETIME = wrapper._driver.DBAPISet(10, 12)

# convertdt not needed b/c it used mx.DateTime
