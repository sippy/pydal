"""
Peter's first stab at a unit test
"""
import unittest
from dal.dbapi.paramstyles import *

SEGMENTIZE_TESTS = [
    [ r'S1', ['S1'] ],
    [ r'"S1"S2', ['"S1"', 'S2'] ],
]

PARAMSTYLE_TESTS = [
    {
        'from'            : 'qmark',
        'to'              : 'qmark',
        'input_query'     : '? ?',
        'expected_query'  : '? ?',
        'input_params'    : [ 1, 2 ],
        'expected_params' : [ 1, 2 ],
    },
    {
        'from'            : 'qmark',
        'to'              : 'numeric',
        'input_query'     : '? ?',
        'expected_query'  : ':1 :2',
        'input_params'    : [ 1, 2 ],
        'expected_params' : [ 1, 2 ],
    },
    {
        'from'            : 'qmark',
        'to'              : 'named',
        'input_query'     : '? ?',
        'expected_query'  : ':param1 :param2',
        'input_params'    : [ 1, 2 ],
        'expected_params' : { 'param1' : 1, 'param2' : 2 },
    },
    {
        'from'            : 'qmark',
        'to'              : 'format',
        'input_query'     : '? ?',
        'expected_query'  : '%s %s',
        'input_params'    : [ 1, 2 ],
        'expected_params' : [ 1, 2 ],
    },
    {
        'from'            : 'qmark',
        'to'              : 'pyformat',
        'input_query'     : '? ?',
        'expected_query'  : '%(param1)s %(param2)s',
        'input_params'    : [ 1, 2 ],
        'expected_params' : { 'param1' : 1, 'param2' : 2 },
    },
]

class SegmentizeTests(unittest.TestCase):

    def setUp(self):
        self.tests = SEGMENTIZE_TESTS

    def tearDown(self):
        del self.tests

    def testSegments(self):
        for test in self.tests:
            input    = test[0]
            expected = test[1]
            actual   = segmentize(input)
            assert actual == expected, 'input=%s, expected=%s, actual=%s' % (input, expected, actual)

class ParamstyleTests(unittest.TestCase):

    def setUp(self):
        self.tests = PARAMSTYLE_TESTS

    def tearDown(self):
        del self.tests

    def testParamstyles(self):
        for test in self.tests:
            from_paramstyle = test['from']
            to_paramstyle   = test['to']
            input_query     = test['input_query']
            expected_query  = test['expected_query']
            input_params    = test['input_params']
            expected_params = test['expected_params']
            actual_query, actual_params = convert( from_paramstyle, to_paramstyle, input_query, input_params )
            assert actual_query == expected_query and actual_params == expected_params, 'from=%s, to=%s, input_query=%s, input_params=%s, expected_query=%s, expected_params=%s, actual_query=%s, actual_params=%s' % (from_paramstyle, to_paramstyle, input_query, input_params, expected_query, expected_params, actual_query, actual_params)


if __name__ == '__main__':
    import os
    cwd = os.getcwd()
    cwds = cwd.split('/')
    dal_dir = '/'.join(cwds[:-3])
    import sys
    sys.path.insert(0, dal_dir)
    import dal
    unittest.main()
