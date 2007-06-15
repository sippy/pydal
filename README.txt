ABOUT
=====

PyDal is a database abstraction layer for Python.  It provides a DBAPI 2.0 wrapper for DBAPI 2.0 drivers.  Sounds strange, but even drivers that fully conform to the DBAPI can differ enough to make building database independent applications difficult.  Two major abstractions handled by PyDal are paramstyles and datetime objects.  PyDal makes it possible to use the same paramstyle and datetime types with any module that conforms to DBAPI 2.0. In addition, paramstyles and datetime types are configurable.

It should work with any driver that is DBAPI 2.0 compliant.  For those that are not, adaptations are handled in configuration files.  Check out config_Example.py for examples.

INSTALL
=======

You can simply copy dal somewhere in your path or use easy_install to install
as an egg.


USAGE
=====

Look at the documentation for the dbapi.py module for a usage example.  A very simple example works like this.

import dal
drv = dal.wrapdriver('psycopg')
cn = drv.connect(database='mydb')
cs = cn.cursor()
cs.execute('select * form mytable')
result = cs.fetchall()

CUSTOM CONFIGURATION
====================

The wrapper should work natively with any DBAPI V2 compliant module, although
some modules may require a configuration file to gain better functionality.
These configuration files should be in the PYTHON PATH (some are included with
this software).

Here are the configuration options.

function convertdt converts the native driver's datetime type to an mxDateTime
or Python datetime object that the wrapper knows how to work with.

quote_chars is a list of characters that should be considered as quote
characters in sql statements not including the sql standard ' chracter.

escape_chars is a list of characters that should be considered as escape
characters that are not standard sql.

function init1 is executed at the beginning of the wrapper initialization and
allows custom modifications to the wrapper or native driver at runtime.

function init2 is executed at the end of the wrapper initialization and
allows custom modifications to the wrapper or native driver at runtime.

There is an example config file nameed config_Example.py

LICENSE
=======

Copyright (c) 2004, Peter Buschman and Randall Smith
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
    * Neither the name of the <ORGANIZATION> nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

AUTHORS
=======

PyDAL is the creation of Randall Smith <randall@tnr.cc> and Peter Buschman <plb@iotk.com>

DOWNLOAD
========

The project is hosted on Sourceforge.

Currently available from SVN:

svn co http://pydal.svn.sourceforge.net/svnroot/pydal pydal
