ABOUT

PyDal is a database abstraction layer for Python.  It provides a DBAPI 2.0 wrapper for DBAPI 2.0 drivers.  Sounds strange, but even drivers that fully conform to the DBAPI can differ enough to make building database independent applications difficult.  Two major abstractions handled by PyDal are paramstyles and datetime objects.  PyDal makes it possible to use the same paramstyle and datetime types with any module that conforms to DBAPI 2.0. In addition, paramstyles and datetime types are configurable.

It should work with any driver that is DBAPI 2.0 compliant.  For those that are not, adaptations are handled in configuration files.  Check out config_Example.py for examples.

AUTHORS

PyDAL is the creation of Randall Smith <randall@tnr.cc> and Peter Buschman <plb@iotk.com>

DOWNLOAD

The project is hosted on Sourceforge.

Currently available from CVS:

cvs -d:pserver:anonymous@cvs.sf.net:/cvsroot/pydal checkout dal

