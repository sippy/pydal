# Thanks to Kevin Jacob's 'Virtual Exceptions'
# http://mail.python.org/pipermail/db-sig/2003-April/003345.html

class Warning:
    pass
class Error(Exception):
    pass
class InterfaceError(Error):
    pass
class DatabaseError(Error):
    pass
class DataError(DatabaseError):
    pass
class OperationalError(DatabaseError):
    pass
class IntegrityError(DatabaseError):
    pass
class InternalError(DatabaseError):
    pass
class ProgrammingError(DatabaseError):
    pass
class NotSupportedError(DatabaseError):
    pass

_dbapi_exceptions = { 'Warning'             : Warning,
                      'Error'               : Error,
                      'InterfaceError'      : InterfaceError,
                      'DatabaseError'       : DatabaseError,
                      'DataError'           : DataError,
                      'OperationalError'    : OperationalError,
                      'IntegrityError'      : IntegrityError,
                      'InternalError'       : InternalError,
                      'ProgrammingError'    : ProgrammingError,
                      'NotSupportedError'   : NotSupportedError }

__all__ = _dbapi_exceptions.keys()

def _setExceptions(wrapper):
    driver = wrapper._driver
    for exception in _dbapi_exceptions.keys():
        dbapi_exception = _dbapi_exceptions[exception]
        sub_exception = getattr(driver, exception)
#        if (not StandardError in sub_exception.mro()):
#            sub_exception.__bases__ += (StandardError, )
        if (not dbapi_exception in sub_exception.mro()):
            sub_exception.__bases__ += (dbapi_exception,)
