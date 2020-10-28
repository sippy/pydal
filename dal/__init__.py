from dal.dbapi.dbapi import wrapdriver
from dal.dbapi.dbexceptions import *
# When I use a relative import, dbapi ends up in the namespace.
#del dbapi
