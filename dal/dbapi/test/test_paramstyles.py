"""
Peter's first stab at a unit test
"""
import unittest

class FakeTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testA(self):
        assert 2 + 2 == 4, 'It isn''t 1984 yet!'

    def testB(self):
        assert 2 + 2 == 5, 'Big Brother is watching you!'


if __name__ == '__main__':
    import os
    cwd = os.getcwd()
    cwds = cwd.split('/')
    dal_dir = '/'.join(cwds[:-3])
    import sys
    sys.path.insert(0, dal_dir)
    import dal
    unittest.main()
